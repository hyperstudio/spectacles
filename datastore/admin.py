# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Document
from .models import Annotation
from .models import Upload
from .models import Archive

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'state', 'created_at', 'updated_at')
    list_filter = ('state', 'created_at', 'updated_at')
    search_fields = ('id', 'creator', 'title',  'author')
    ordering = ('id',)

class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'creator', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('uuid', 'creator')
    ordering = ('created_at',)

class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'state', 'content_type', 'created_at', 'updated_at')
    list_filter = ('state', 'created_at', 'updated_at')
    search_fields = ('creator', 'state', 'content_type')
    ordering = ('id',)

class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'title')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('id',)

admin.site.register(Document, DocumentAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Upload, UploadAdmin)
admin.site.register(Archive, ArchiveAdmin)
