from django.conf import settings

from webkassa.settings import apply_default_settings

assert hasattr(settings, 'WEBKASSA_CONFIG'), 'Please add required attribute `WEBKASSA_CONFIG` to your settings.py'
assert 'api_key' in settings.WEBKASSA_CONFIG, 'Please add required attribute `api_key` to `WEBKASSA_CONFIG`'
assert 'url' in settings.WEBKASSA_CONFIG, 'Please add required attribute `url` to `WEBKASSA_CONFIG`'
assert 'encryption_key' in settings.WEBKASSA_CONFIG, \
    'Please add required attribute `encryption_key` to `WEBKASSA_CONFIG`'

apply_default_settings()
