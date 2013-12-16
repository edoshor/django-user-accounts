from __future__ import unicode_literals

from django.db.models import Q

try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from account.future_1_5 import get_user_model
from django.contrib.auth.backends import ModelBackend

from account.models import EmailAddress


class UsernameAuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        User = get_user_model()
        try:
            user = User.objects.get(username__iexact=credentials["username"])
        except (User.DoesNotExist, KeyError):
            return None
        else:
            try:
                if user.check_password(credentials["password"]):
                    return user
            except KeyError:
               return None 

class EmailAuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        qs = EmailAddress.objects.filter(Q(primary=True) | Q(verified=True))
        try:
            email_address = qs.get(email__iexact=credentials["username"])
        except (EmailAddress.DoesNotExist, KeyError):
            return None
        else:
            user = email_address.user
            try:
                if user.check_password(credentials["password"]):
                    return user
            except KeyError:
                return None
