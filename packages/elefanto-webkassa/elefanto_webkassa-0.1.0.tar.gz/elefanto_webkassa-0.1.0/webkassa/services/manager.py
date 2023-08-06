from django.conf import settings
from django.utils.translation import gettext_lazy as _

import httpx
from httpx import ConnectTimeout

from rest_framework.exceptions import AuthenticationFailed, ValidationError

from webkassa.models import Check, WebKassaAccount
from webkassa.serializers import CheckSerializer

WEBKASSA_CONFIG = settings.WEBKASSA_CONFIG
URL = WEBKASSA_CONFIG['url'] if WEBKASSA_CONFIG['is_prod'] else WEBKASSA_CONFIG['test_url']
API_KEY = WEBKASSA_CONFIG['api_key'] if WEBKASSA_CONFIG['is_prod'] else WEBKASSA_CONFIG['test_api_key']
HEADERS = {'X-API-KEY': API_KEY, 'Content-Type': 'application/json'}


class WebKassaManager:
    _token: str = None
    _email: str = None
    cashier: WebKassaAccount = None
    _client: httpx.Client = None

    def __init__(self, email: str):
        self._email = email
        self.cashier = self._get_cashier()
        self._token = self.cashier.token
        self._client = httpx.Client()

    def _get_cashier(self) -> WebKassaAccount:
        try:
            return WebKassaAccount.objects.get(
                email=self._email,
            )
        except WebKassaAccount.DoesNotExist:
            raise ValidationError(_('WebKassaAccount does not exist ({email})'.format(email=self._email)))

    def login(self):
        url = f'{URL}/api/Authorize'
        data = {'Login': self.cashier.email,
                'Password': self.cashier.decrypted_password}

        response = self._client.post(url, json=data, headers=HEADERS, timeout=10)

        if response.status_code == 200:

            if 'Data' not in response.json():
                raise AuthenticationFailed(
                    detail={'detail': _('Error in login to web kassa: {email}'.format(email=self._email))})

            self._token = response.json()['Data']['Token']

            self.cashier.token = self._token
            self.cashier.save()
        else:
            raise AuthenticationFailed(
                detail={'detail': _('Error in login to web kassa: {email}'.format(email=self._email))})

    def close_cash_box(self):
        try:
            url = f'{URL}/api/ZReport'

            data = {
                'Token': self._token,
                'CashboxUniqueNumber': self.cashier.cashbox_unique_number,
            }
            self._client.post(url, json=data, headers=HEADERS, timeout=10)
        except ConnectTimeout as e: # noqa
            # TODO logging
            pass

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

        url = f'{URL}/api/Check'
        data.update({
            'ExternalCheckNumber': str(check_obj.id),
        })
        try:
            response = self._client.post(url, json=data, headers=HEADERS, timeout=10).json()
            if 'Data' in response:
                check = response['Data']
                check_serializer = CheckSerializer(check_obj, data=check, partial=True)
                check_serializer.is_valid(raise_exception=True)
                check_serializer.save()
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
                        # TODO logging
                        pass

        except ConnectTimeout:
            # TODO logging
            return self._create_check(data, check_obj=check_obj)
        except Exception as e: # noqa
            # TODO logging
            pass
        return check_obj

    def get_check(self, data: dict):
        data = self._set_positions_default(data)
        data['Token'] = self._get_web_kassa_token()
        data['CashboxUniqueNumber'] = self.cashier.cashbox_unique_number
        data = self._calculate_tax(data)
        profile_id = data.pop('profile_id') if 'profile_id' in data else None
        return self._create_check(data, profile_id)
