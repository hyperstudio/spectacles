# coding: utf-8
from __future__ import print_function, unicode_literals
import uuid


from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import JSONField
from django.db import models

from enumfields import Enum
from enumfields import EnumIntegerField
from enumfields import IntEnum

from spectacles.vectors import vector_from_html_text
from spectacles.utils import DictModel
from spectacles.utils import VectorModel


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

class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='archives',
    )
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


class DocumentState(IntEnum):
    DELETED = 0
    DRAFT = 1
    PUBLISHED = 2


class TextFreeDocumentManager(models.Manager):
    def slim(self):
        return super(TextFreeDocumentManager, self).get_queryset().defer('text')

class Document(VectorModel, DictModel, models.Model):
    _json_fields = (
            'id', 'title', 'created_at', 'updated_at', 'text', 'author',
            'creator')
    _slim_fields = (
            'id', 'title', 'created_at', 'updated_at', 'author',
            'creator')

    slim = TextFreeDocumentManager()
    objects = models.Manager()

    # Internal
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='documents',
    )
    upload = models.ForeignKey(
        'spectacles.Upload',
        null=True,
        related_name='documents',
    )
    # Data
    state = EnumIntegerField(DocumentState)
    title = models.TextField(null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    author = models.TextField(null=False, blank=False)
    vector = models.BinaryField(null=True, blank=False)
    vector_needs_synch = models.BooleanField(default=True, blank=False)

    def recalculate_vector(self):
        v = vector_from_html_text(self.text)
        if v is not None:
            self.set_vector(v)
        return v

    def save(self, *args, **kwargs):
        #if not self.has_vector() and self.text:
        #    self.recalculate_vector()
        return super(Document, self).save(*args, **kwargs)

class UploadState(Enum):
    NEW = 0
    PROCESSING = 1
    COMPLETE = 2

class Upload(models.Model):
    # Internal
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='uploads',
    )
    # Data
    state = EnumIntegerField(UploadState)
    source_file = models.FileField(upload_to='uploads/', max_length=256)
    content_type = models.CharField(max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


class WithDocumentInformation(models.Manager):
    def with_doc_info(self):
        return (super(WithDocumentInformation, self)
            .get_queryset()
            .annotate(document_title=models.F('document__title')))

class Annotation(VectorModel, DictModel, models.Model):
    document_title=''
    _json_fields = (
            'id', 'uuid', 'creator', 'created_at', 'updated_at',
            'data', 'document_id', 'document_title', 'quote', 'text', 'tags')

    objects = WithDocumentInformation()

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # Internal
    document = models.ForeignKey(
        'spectacles.Document',
        null=True,
        related_name='annotations'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='annotations',
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    # Data
    data = JSONField()
    vector = models.BinaryField(null=True, blank=False)
    vector_needs_synch = models.BooleanField(default=True, blank=False)

    @property
    def quote(self):
        return self.data.get('quote', '')

    @property
    def text(self):
        return self.data.get('text', '')

    @property
    def tags(self):
        return self.data.get('tags', [])

    def recalculate_vector(self):
        v1 = vector_from_html_text(self.text)
        v2 = vector_from_html_text(self.quote)
        if v1 is not None and v2 is not None:
            v = (v1 + v2) / 2
        elif v1 is not None:
            v = v1
        elif v2 is not None:
            v = v2
        else:
            v = None

        if v is not None:
            self.set_vector(v)
        return v

    def save(self, *args, **kwargs):
        #if not self.has_vector() and self.text:
        #    self.recalculate_vector()
        return super(Annotation, self).save(*args, **kwargs)

class Bookmark(DictModel, models.Model):
    _json_fields = ('id',)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    document = models.ForeignKey( # Mandatory, always link to a document
        'spectacles.Document',
        null=False,
        related_name='bookmarks',
    )
    annotation = models.ForeignKey( # Optional, link to a specific annotation
        'spectacles.Annotation',
        null=True,
        related_name='bookmarks',
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='bookmarks',
    )
