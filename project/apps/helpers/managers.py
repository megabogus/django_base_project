from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager



class DeletedQueryMixin(models.query.QuerySet):
    def delete(self, force=False):
        if force:
            return super().delete()
        else:
            return self._delete()

    def _delete(self):
        return (self.count(), self.update(deleted_at=timezone.now()))

    def deleted(self):
        return self.filter(deleted_at__isnull=False)

    def non_deleted(self):
        return super().filter(deleted_at__isnull=True)


class DeletedQuerySet(DeletedQueryMixin, models.query.QuerySet):
    pass


class DeletedManager(UserManager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.get_queryset().deleted()

    def non_deleted(self):
        return self.get_queryset().non_deleted()


