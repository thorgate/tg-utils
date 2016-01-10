from django.db import models
from django.utils import timezone

from tg_utils.signals import post_modify


class ClosableObjectsQuerySet(models.QuerySet):
    """ Provides easy way to mark ClosableModel objects as closed
    """
    def close(self, user):
        return self.update(closed_at=timezone.now(), closed_by=user)


class NotClosedObjectsManager(models.Manager.from_queryset(ClosableObjectsQuerySet)):
    """ Utility manager that excludes items that have non-null closed_by value
    """
    def get_queryset(self):
        return super().get_queryset().filter(closed_by=None)


class NotifyPostChangeQuerySet(models.QuerySet):
    """ Sends out a signal (post_modify) whenever anything modifies the database [*]

    Note that the signals are sent out immediately and won't be deferred until the current database transaction (if any)
    is committed.

    [*] except save() and delete() methods of the model. You should explicitly listen to those yourself.
    """
    def delete(self):
        return self.with_signal(super().delete())

    def create(self, **kwargs):
        return self.with_signal(super().create(**kwargs))

    def update(self, **kwargs):
        return self.with_signal(super().update(**kwargs))

    def bulk_create(self, *args, **kwargs):
        return self.with_signal(super().bulk_create(*args, **kwargs))

    def update_or_create(self, *args, **kwargs):
        """ Only sent when not created, since default implementation will
            call `self.create` when creating which triggers our signal
            already.
        """
        obj, created = super().update_or_create(*args, **kwargs)

        if not created:
            return self.with_signal(result=(obj, created))

        return obj, created

    def with_signal(self, result):
        # Trigger the post_change signal
        post_modify.send(sender=self.model)

        # Return the original result
        return result


NotifyModificationsManager = models.Manager.from_queryset(NotifyPostChangeQuerySet)
