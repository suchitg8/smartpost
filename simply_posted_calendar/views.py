from django.core import serializers
from django.http import HttpResponse, JsonResponse

from django.db.models import F

from django.contrib.auth.models import User
from simply_posted_calendar.models import Publication
from simply_posted_accounts.models import Post

from publishing import PublishingService
from select_posts import ContentSelectionService

def get_all(request):
    publications = to_dict(Publication.objects.filter(user=request.user))
    return JsonResponse(publications, safe=False)

def approve(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(approved=True) 

    data = publication.values().first()
    return JsonResponse(data)

def reject(request, pk):
    publication = Publication.objects.filter(pk=pk)
    publication.update(reject_count=F('reject_count') + 1)

    substituted_post = substitute(publication.first())
    if substituted_post:
        data = to_dict([substituted_post])
    else:
      data = []

    return JsonResponse(data, safe=False)

def get_new(request):
    publications = ContentSelectionService(request.user).make_publications()
    return JsonResponse(to_dict(publications), safe=False)

def to_dict(publications):
    result = []
    for publication in publications:
        color = '#449d44' if publication.approved else '#c9302c' if publication.approved == False else '#337ab7'
        title = publication.post.corporate_title if publication.corporate_title else publication.post.playful_title

        publication_data = {'title': title, 'content': publication.post.blog_link, 'start': publication.publication_date.isoformat(), 'id': publication.id, 'color': color, 'reject_count': publication.reject_count, 'approved': publication.approved}
        result.append(publication_data)

    return result

def substitute(publication):
    if publication.reject_count >= 3:
        publication.approved = False
        publication.save()
        return False


    new_id = Post.objects.filter(category=publication.post.category).exclude(users=publication.user).first()
    publication.post_id = new_id
    publication.save()

    return publication
