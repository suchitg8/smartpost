from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()
    published = models.BooleanField(default=False)
    approved = models.NullBooleanField()
    substituted_for = models.ForeignKey('self', null=True, blank=True)
