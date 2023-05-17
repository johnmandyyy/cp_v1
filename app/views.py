"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

from .forms import *


from rest_framework import generics
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend


class ChickensListCreateView(generics.ListCreateAPIView):
    queryset = Chickens.objects.all()
    serializer_class = ChickensSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_infected']

class ChickensRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chickens.objects.all()
    serializer_class = ChickensSerializer
    lookup_field = 'id'  # Set the lookup_field to 'id'


class ChickenHistoryListCreateView(generics.ListCreateAPIView):
    queryset = ChickenHistory.objects.all()
    serializer_class = ChickenHistorySerializer

class ChickenHistoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChickenHistory.objects.all()
    serializer_class = ChickenHistorySerializer
    lookup_field = 'chicken'  # Set the lookup_field to 'id'








def home(request):
    """Renders the home page."""


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'add_chicken': ChickensForm(),
            'add_history': ChickenHistoryForm(),
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
