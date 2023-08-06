from webkassa.models import WebKassaAccount, WebkassaErrorLog
from webkassa.services.manager import WebKassaManager


def close_cash_box():
    cashboxes = []
    for account in WebKassaAccount.objects.all():
        if account.cashbox_unique_number not in cashboxes:
            try:
                instance = WebKassaManager(email=account.email, cashbox_unique_number=account.cashbox_unique_number)
                instance.login()
                instance.close_cash_box()
                cashboxes.append(account.cashbox_unique_number)
            except Exception as e:
                WebkassaErrorLog.objects.create(
                    code=-10,
                    text=f'error in cron: {account.email}({account.cashbox_unique_number}) \n{str(e)}',
                )
