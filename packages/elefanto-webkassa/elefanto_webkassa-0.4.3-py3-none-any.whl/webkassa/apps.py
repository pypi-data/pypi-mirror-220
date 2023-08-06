from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebkassaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webkassa'
    verbose_name = _('Webkassa')
