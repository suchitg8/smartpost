from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from simply_posted_accounts.models import Post

class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post)
    publication_date = models.DateTimeField()
    published = models.BooleanField(default=False)
    approved = models.NullBooleanField()
    substituted_for = models.ForeignKey('self', null=True, blank=True)
    reject_count = models.PositiveIntegerField(default=0)
    corporate_title = models.BooleanField(default=True)
