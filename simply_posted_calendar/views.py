from django.core import serializers
from django.http import JsonResponse

from calendarium.models import Event

def approve(request, pk):
    return JsonResponse({'id': pk})

def reject(request, pk):
    return JsonResponse({'id': pk})
