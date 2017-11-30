from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

from app.utils import DictModel


class UserManager(BaseUserManager):
    def _create_user(self, email, password, name, **extra_fields):
        if not email:
            raise ValueError('missing email')
        if not password:
            raise ValueError('missing password')
        if not name:
            raise ValueError('missing name')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('cannot create superuser without is_superuser=True')
        if not extra_fields.get('is_active'):
            raise ValueError('cannot create superuser without is_active=True')

        return self._create_user(email, password, name, **extra_fields)


class User(DictModel, AbstractBaseUser):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    _json_fields = (
            'id', 'email', 'name', 'last_login',
            'date_joined', 'is_active', 'is_superuser')

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    name = models.TextField(unique=False, null=False, blank=False)
    last_login = models.DateTimeField(auto_now=True, null=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)

    # Set to false to soft-delete an account.
    is_active = models.BooleanField(default=True, null=False)
    # Also grants access to the admin site.
    is_superuser = models.BooleanField(default=False, null=False)

    # Django Internal

    def __unicode__(self):
        return self.email

    def __str__(self):
        return str(self.email)

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def get_full_name(self):
        return self.name

    @property
    def get_short_name(self):
        return self.name

    # Django Admin
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
