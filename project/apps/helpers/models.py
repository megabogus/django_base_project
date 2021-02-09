import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import DeletedManager


class BaseConsumerAbstractModel(models.Model):
    """
    An abstract base class that any custom models probably should
    subclass.
    """
    consumer_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Consumer Type"),
        related_name="content_type_set_for_%(class)s",
        blank=True, null=True, on_delete=models.SET_NULL
    )
    consumer_pk = models.PositiveIntegerField(_("Consumer ID"))
    consumer = GenericForeignKey(
        ct_field="consumer_type", fk_field="consumer_pk")

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    created_at = models.DateTimeField(_('создан'), auto_now_add=True)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    deleted_at = models.DateTimeField(_('удален'), null=True, blank=True, editable=False)

    objects = DeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()
            self.save()


class CreatedDeletedModel(CreatedModel, DeletedModel):
    class Meta:
        abstract = True
