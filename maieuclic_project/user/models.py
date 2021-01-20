from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class MaieuclicUserManager(BaseUserManager):
    pass


class MaieuclicUser(AbstractBaseUser, PermissionsMixin):
    pass
