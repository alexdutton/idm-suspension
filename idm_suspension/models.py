from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
import django_fsm


class FSMBooleanField(django_fsm.FSMFieldMixin, models.BooleanField):
    """
    Same as FSMField, but stores the state value in a BooleanField.
    """
    pass


class SuspensionCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    label = models.CharField(max_length=256)


class Suspension(models.Model):
    object_id = models.CharField(max_length=256)
    content_type = models.ForeignKey(ContentType, related_name='suspensions')
    object = GenericForeignKey()

    category = models.ForeignKey(SuspensionCategory, null=True, blank=True)

    owner_id = models.CharField(max_length=256, null=True, blank=True)
    owner_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name='owned_suspensions')
    owner = GenericForeignKey('owner_content_type', 'owner_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(null=True, blank=True)

    user_reason = models.TextField()
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.start:
            self.start = now()
        return super().save(*args, **kwargs)


class Suspendable(models.Model):
    suspended = FSMBooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)

    @django_fsm.transition(suspended, target=True)
    def suspend(self, user, category=None, owner=None, start=None, end=None, user_reason='', notes=''):
        suspension = Suspension(object=self,
                                user=user,
                                category=category,
                                owner=owner,
                                start=start or now(),
                                end=end, user_reason=user_reason, notes=notes)
        if self.suspended:
            self.suspended_until = max(self.suspended_until, end) if self.suspended_until and end else None
        else:
            self.suspended_until = end

        suspension.save()

    class Meta:
        abstract = True