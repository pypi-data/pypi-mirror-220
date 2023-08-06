from django.db import models
from django.utils.translation import gettext_lazy as _

from webkassa.services.password_encryption import decrypt_password, encrypt_password


class Check(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    ticket_url = models.URLField(blank=True, null=True, verbose_name=_('Ticket URL'))
    ticket_print_url = models.URLField(blank=True, null=True, verbose_name=_('Ticket URL for print'))
    check_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Check number'))
    date_time = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Check datetime'))
    cash_box = models.JSONField(blank=True, null=True, verbose_name=_('Cashbox'))
    check_order_number = models.BigIntegerField(default=0, verbose_name=_('Check order number'))
    shift_number = models.BigIntegerField(default=0, verbose_name=_('Shift number'))
    employee_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Employee name'))

    def __str__(self):
        return 'Check #{order_id}'.format(order_id=self.pk) # noqa

    class Meta:
        verbose_name = _('Check')
        verbose_name_plural = _('Checks')


class WebKassaAccount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    cashbox_unique_number = models.CharField(max_length=255)

    is_encrypted = models.BooleanField(default=False)

    token = models.CharField(max_length=100, default='')

    @property
    def decrypted_password(self):
        if self.is_encrypted:
            return decrypt_password(self.password)
        return self.password

    def save(self, *args, **kwargs):
        if not self.is_encrypted:
            self.password = encrypt_password(self.password)
            self.is_encrypted = True
        super(WebKassaAccount, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Webkassa account')
        verbose_name_plural = _('Webkassa accounts')
