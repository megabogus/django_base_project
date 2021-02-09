from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from fieldsignals import post_save_changed

User = get_user_model()


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = _('Управление пользователями')

    def ready(self):
        from .signals import change_staff_perms, set_default_perms_to_user, set_perms_to_staff
        post_save_changed.connect(change_staff_perms, sender=User, fields=('is_staff',))
        post_save.connect(set_default_perms_to_user, sender=User)
        post_save.connect(set_perms_to_staff, sender=User)
        return super().ready()
