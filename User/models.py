from django.db import models
from SCOM_APP.models import InfoGuru
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class LoginGuru(AbstractUser):
    username = models.CharField(max_length = 25, unique=True)
    password = models.CharField(max_length = 25)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    subject = models.ForeignKey(InfoGuru, on_delete=models.CASCADE, default=1)
    test = models.CharField(max_length = 25)
