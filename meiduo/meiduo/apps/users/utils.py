import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def user_mobile_check(account):
    try:
        if re.match(r'^1[345789]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except Exception:
        return None

    return user


class UsernameMobileCheckModel(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = user_mobile_check(username)
        if user and user.check_password(password):
            return user
