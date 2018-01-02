from django.conf import settings
from django.db import models
from django.utils import timezone

from .managers import NotClosedObjectsManager


class ClosableModel(models.Model):
    """ Model that can be soft-deleted (closed).

    Contains timestamp and user for both creation and closing.
    Also provides default manager that automatically filters queryset to only include active (non-closed) items plus a
    .close() function to mark objects as closed.
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    all_objects = models.Manager()
    objects = NotClosedObjectsManager()

    class Meta:
        abstract = True

    def close(self, user):
        self.closed_by = user
        self.closed_at = timezone.now()
        self.save()


class TimestampedModel(models.Model):
    """ Provides self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ClosableTimestampedModel(ClosableModel):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
