from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

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


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
