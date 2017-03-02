from django.core import serializers
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from simply_posted_calendar.models import Publication

def get_all(request):
    publications = to_dict(Publication.objects.all().exclude(approved=False))
    return JsonResponse(publications, safe=False)

def approve(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(approved=True) 

    data = publication.values().first()
    return JsonResponse(data)

def reject(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(approved=False)

    substituted_post = substitute(publication.first())
    if substituted_post:
        data = to_dict([substituted_post])
    else:
      data = []

    return JsonResponse(data, safe=False)

def get_new(request):
    user = User.objects.first()
    publications = [Publication(user=user, publication_date=datetime.datetime.now() + datetime.timedelta(days=n+1)) for n in range(10)]
    return JsonResponse({ "publications": Publication.objects.all().values() })

def to_dict(publications):
    result = []
    for publication in publications:
        color = '#449d44' if publication.approved else '#c9302c' if publication.approved == False else '#337ab7'
        publication_data = {'title': 'test', 'content': 'test', 'start': publication.publication_date.isoformat(), 'id': publication.id, 'color': color}
        result.append(publication_data)

    return result

def substitute(publication):
    if publication.substituted_for and publication.substituted_for.substituted_for:
        return False

    user = publication.user
    substitute = Publication.objects.create(publication_date=publication.publication_date, user=publication.user, substituted_for=publication)

    return substitute
