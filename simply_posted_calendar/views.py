from django.core import serializers
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from simply_posted_calendar.models import Publication

def get_all(request):
    publications = Publication.objects.all().values()
    return JsonResponse({ "publications": list(publications) })

def approve(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(approved=True) 

    data = publication.values().first()
    return JsonResponse(data)

def reject(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(approved=False)

    data = publication.values().first()
    return JsonResponse(data)

def get_new(request):
    user = User.objects.first()
    publications = [Publication(user=user, publication_date=datetime.datetime.now() + datetime.timedelta(days=n+1)) for n in range(10)]
    return JsonResponse({ "publications": Publication.objects.all().values() })
