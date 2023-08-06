from cryptography.fernet import Fernet

from django.conf import settings


def encrypt_password(raw_password):
    fernet = Fernet(settings.WEBKASSA_CONFIG['encryption_key'])
    return fernet.encrypt(raw_password.encode()).decode()


def decrypt_password(password):
    fernet = Fernet(settings.WEBKASSA_CONFIG['encryption_key'])
    return fernet.decrypt(bytes(password, 'ascii')).decode()
