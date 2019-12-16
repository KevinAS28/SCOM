from django.conf import settings
from django.contrib.auth.hashers import check_password
from User.models import LoginGuru


class AuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        data = LoginGuru.objects.filter(username=username, password=password)
        if len(data)==0:
            return None
        else:
            return data[0]

    def get_user(self, username):
        try:
            return LoginGuru.objects.get(username=username)
        except LoginGuru.DoesNotExist:
            return None