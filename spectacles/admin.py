# coding: utf-8
from __future__ import unicode_literals, print_function
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from .models import Document
from .models import Annotation
from .models import Upload
from .models import Archive

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('email', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )
    filter_horizontal = ()

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

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Upload, UploadAdmin)
admin.site.register(Archive, ArchiveAdmin)
