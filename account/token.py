from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import datetime


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,data,timestamp):
        now = datetime.datetime.now()
        return six.text_type(data['email']) + six.text_type(now) + six.text_type(data['first_name'])

account_activation_token = TokenGenerator()