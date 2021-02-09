from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from guardian.shortcuts import assign_perm, remove_perm


def set_default_perms_to_user(sender, instance=None, created=False, **kwargs):
    if instance.username != "AnonymousUser":
        if not instance.has_perm('accounts.change_user', instance):
            assign_perm('accounts.change_user', instance)
            assign_perm('accounts.change_user', instance, instance)
        if not instance.has_perm('accounts.view_user', instance):
            assign_perm('accounts.view_user', instance)
            assign_perm('accounts.view_user', instance, instance)


def set_perms_to_staff(sender, instance=None, created=False, **kwargs):
    users = sender.objects.all()
    if created and instance.is_staff:
        assign_perm('accounts.add_user', instance)
        assign_perm('accounts.change_user', instance)
        assign_perm('accounts.change_user', instance, users)
        assign_perm('accounts.view_user', instance)
        assign_perm('accounts.view_user', instance, users)


def change_staff_perms(sender, instance=None, changed_fields=None, **kwargs):
    users = sender.objects.all()
    for field, (old, new) in changed_fields.items():
        if field.name == 'is_staff':
            if new:
                assign_perm('accounts.add_user', instance)
                assign_perm('accounts.change_user', instance)
                assign_perm('accounts.change_user', instance, users)
                assign_perm('accounts.view_user', instance)
                assign_perm('accounts.view_user', instance, users)
            else:
                remove_perm('accounts.add_user', instance)
                remove_perm('accounts.change_user', instance)
                remove_perm('accounts.change_user', instance, users)
                remove_perm('accounts.view_user', instance)
                remove_perm('accounts.view_user', instance, users)