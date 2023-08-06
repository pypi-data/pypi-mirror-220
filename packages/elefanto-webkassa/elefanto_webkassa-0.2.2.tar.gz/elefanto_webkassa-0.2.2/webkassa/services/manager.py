import json

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import httpx
from httpx import ConnectTimeout

from rest_framework.exceptions import AuthenticationFailed, ValidationError

from webkassa.models import Check, WebKassaAccount, WebkassaErrorLog
from webkassa.serializers import CheckSerializer

WEBKASSA_CONFIG = settings.WEBKASSA_CONFIG
URL = WEBKASSA_CONFIG['url']
HEADERS = {'X-API-KEY': WEBKASSA_CONFIG['api_key'], 'Content-Type': 'application/json'}


class WebKassaManager:
    _token: str = ''
    _email: str = ''
    cashier: WebKassaAccount = None
    _client: httpx.Client = None
    _url: str = URL
    _headers: dict = HEADERS
    _cashbox_unique_number: str = ''

    def __init__(self, email: str, cashbox_unique_number: str, url: str = URL, headers: dict = HEADERS): # noqa
        self._email = email
        self._cashbox_unique_number = cashbox_unique_number
        self.cashier = self._get_cashier()
        self._token = self.cashier.token
        self._client = httpx.Client()
        self._url = url
        self._headers = headers

    def _get_cashier(self) -> WebKassaAccount:
        try:
            return WebKassaAccount.objects.get(
                email=self._email,
                cashbox_unique_number=self._cashbox_unique_number
            )
        except WebKassaAccount.DoesNotExist:
            WebkassaErrorLog.objects.create(
                code=-1,
                text='WebKassaAccount does not exist ({email}, {number})'.format(
                    email=self._email, number=self._cashbox_unique_number),
            )

    def login(self):
        if self.cashier:
            url = f'{URL}/api/Authorize'
            data = {'Login': self.cashier.email,
                    'Password': self.cashier.decrypted_password}

            response = self._client.post(url, json=data, headers=self._headers, timeout=30)

            if response.status_code == 200:

                if 'Data' not in response.json():
                    WebkassaErrorLog.objects.create(
                        code=-2,
                        text='Error in login to web kassa: {email}'.format(email=self._email),
                    )
                    self._token = '-1'
                    return

                self._token = response.json()['Data']['Token']

                self.cashier.token = self._token
                self.cashier.save()
            else:
                WebkassaErrorLog.objects.create(
                    code=-2,
                    text='Error in login to web kassa: {email}'.format(email=self._email),
                )
                self._token = '-1'

    def close_cash_box(self):
        try:
            url = f'{self._url}/api/ZReport'

            data = {
                'Token': self._token,
                'CashboxUniqueNumber': self.cashier.cashbox_unique_number,
            }
            self._client.post(url, json=data, headers=self._headers, timeout=30)
        except ConnectTimeout:
            WebkassaErrorLog.objects.create(
                code=-1,
                text='Connect Timeout on close_cash_box',
            )

    def _get_web_kassa_token(self):
        if not self._token:
            self.login()
            return self._get_web_kassa_token()
        return self._token

    @staticmethod
    def _set_positions_default(data):
        for position in data['Positions']:
            position['Tax'] = round(float(position['Price']) - (float(position['Price']) * 100)
                                    / (float(position['TaxPercent']) + 100), 2)
        return data

    @staticmethod
    def _calculate_tax(data: dict):
        modifiers = data.get('TicketModifiers')
        if modifiers:
            new_modifiers = []
            for modifier in modifiers:
                if 'Tax' not in modifier:
                    modifier['Tax'] = round(float(modifier['Sum']) - (float(modifier['Sum']) * 100)
                                            / (float(modifier['TaxPercent']) + 100), 2)
                new_modifiers.append(modifier)
            data.update({
                'TicketModifiers': new_modifiers,
            })
        return data

    @staticmethod
    def _prepare_check():
        return Check.objects.create()

    def _create_check(self, data, check_obj=None):

        if not check_obj:
            check_obj = self._prepare_check()

        url = f'{self._url}/api/Check'
        try:
            response = self._client.post(url, json=data, headers=HEADERS, timeout=30).json()
            if 'Data' in response:
                check = response['Data']
                check_serializer = CheckSerializer(check_obj, data=check, partial=True)
                if check_serializer.is_valid():
                    check_serializer.save()
                else:
                    WebkassaErrorLog.objects.create(
                        code=-4,
                        text='CheckSerializer validation: {data}'.format(data=check),
                    )
            elif 'Errors' in response:
                errors = response['Errors']
                for error in errors:
                    if error['Code'] in [3, 2, 1]:
                        self.login()
                        data.update({
                            'Token': self._get_web_kassa_token(),
                        })
                        return self._create_check(data, check_obj=check_obj)
                    elif error['Code'] == 11:
                        self.close_cash_box()
                        return self._create_check(data, check_obj=check_obj)
                    else:
                        WebkassaErrorLog.objects.create(
                            check=check_obj,
                            code=error['Code'],
                            text=error.get('Text', json.dumps(error)),
                        )

        except ConnectTimeout:
            WebkassaErrorLog.objects.create(
                check=check_obj,
                code=-1,
                text='Connect Timeout on _create_check with data {data}'.format(data=json.dumps(data)),
            )
            return self._create_check(data, check_obj=check_obj)
        except Exception as e: # noqa
            WebkassaErrorLog.objects.create(
                check=check_obj,
                code=-3,
                text=str(e),
            )
        return check_obj

    def get_check(self, data: dict):
        data = self._set_positions_default(data)
        data['Token'] = self._get_web_kassa_token()
        if self._token == '-1':
            return None
        data['CashboxUniqueNumber'] = self.cashier.cashbox_unique_number
        data = self._calculate_tax(data)
        return self._create_check(data)
