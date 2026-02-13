from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import datetime

fernet = Fernet(settings.FIELD_ENCRYPTION_KEY)


class EncryptedTextField(models.TextField):

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return fernet.encrypt(value.encode()).decode()
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            return value


class EncryptedDateField(models.DateField):

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.date):
            value = value.isoformat()
        return fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            decrypted = fernet.decrypt(value.encode()).decode()
            return datetime.date.fromisoformat(decrypted)
        except Exception:
            return value
