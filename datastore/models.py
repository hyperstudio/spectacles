# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

from enumfields import EnumIntegerField
from enumfields import Enum

# Create your models here.

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


class DocumentState(Enum):
    DELETED = 0
    DRAFT = 1
    PUBLISHED = 2

class Document(models.Model):
    # Internal
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='documents',
    )
    upload = models.ForeignKey(
        'datastore.Upload',
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

class Annotation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Internal
    document = models.ForeignKey(
        'datastore.Document',
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
