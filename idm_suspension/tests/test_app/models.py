from django.db import models

from idm_suspension.models import Suspendable


class Entitlement(Suspendable, models.Model):
    pass
