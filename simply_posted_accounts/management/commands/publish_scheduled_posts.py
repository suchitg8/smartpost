import datetime

from django.core.management.base import BaseCommand, CommandError
from simply_posted_calendar.models import Publication
from publishing import PublishingService

class Command(BaseCommand):
    def handle(self, *args, **options):
        publications = Publication.objects.filter(approved=True, published=False, publication_date__lte=datetime.datetime.now())
        
        for publication in publications:
            profiles = publication.user.social_auth.all()
            PublishingService(profiles, publication.post).publish_post()

            publication.published = True
            publication.save()
