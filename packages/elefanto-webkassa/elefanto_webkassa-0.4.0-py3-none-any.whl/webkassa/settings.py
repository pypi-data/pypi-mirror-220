from django.conf import settings


def apply_default_settings():
    settings.INSTALLED_APPS.append('django_crontab')
    cronjob = ('0 0 * * *', 'myapp.cron.my_scheduled_job')
    if hasattr(settings, 'CRONJOBS'):
        settings.CRONJOBS.append(cronjob)
    else:
        settings.CRONJOBS = [
            cronjob,
        ]
