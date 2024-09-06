from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from utility.models import BaseModel

class CustomUser(AbstractUser,BaseModel):
    email = models.EmailField(
        _('email address'), unique=True, max_length=200, blank=False, null=False)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='media',null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]