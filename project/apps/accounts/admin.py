from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django_history.admin import HistoryBlockAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(HistoryBlockAdmin, BaseUserAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_display_links = ('pk', 'username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Персональная информация'),
            {
                'fields': (
                    'first_name',
                    'middle_name',
                    'last_name',
                    'birthday',
                    'gender',
                    'photo',
                )
            },
        ),
        (_('Контактная информация'), {'fields': ('phone', 'email',)}),
        (_('Доступы'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'change_password', 'date_joined', 'deleted_at')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'username', 'email', 'phone', 'password1', 'password2')
                             }),)

    readonly_fields = ('last_login', 'change_password', 'date_joined', 'deleted_at')
