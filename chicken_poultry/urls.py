"""
Definition of urls for chicken_poultry.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


from app.views import ChickensListCreateView, ChickensRetrieveUpdateDestroyView, ChickenHistoryListCreateView, ChickenHistoryRetrieveUpdateDestroyView, DiseaseListCreateView 
from app.views import DiseaseRetrieveUpdateDestroyView, SymptomsListCreateView, SymptomsDestroyAll, SymptomsListCreateRandom
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('getprediction', views.getPrediction, name='getprediction'),
    path('admin', admin.site.urls),
    path('api/symptoms/create-random/', SymptomsListCreateRandom.as_view(), name='symptoms-random-create'),
    path('api/symptoms/destroy-all/', SymptomsDestroyAll.as_view(), name='symptoms-destroy-all'),
    path('api/symptoms/', SymptomsListCreateView.as_view(), name='symptoms-list-create'),
    path('api/diseases/', DiseaseListCreateView.as_view(), name='diseases-list-create'),
    path('api/diseases/<int:pk>/', DiseaseRetrieveUpdateDestroyView.as_view(), name='diseases-retrieve-update-destroy'),
    path('api/chickens/', ChickensListCreateView.as_view(), name='chickens-list-create'),
    path('api/chickens/<int:id>/', ChickensRetrieveUpdateDestroyView.as_view(), name='chickens-retrieve-update-destroy'),
    path('api/chicken-history/', ChickenHistoryListCreateView.as_view(), name='chicken-history-list-create'),
    path('api/chicken-history/<int:id>/', ChickenHistoryRetrieveUpdateDestroyView.as_view(), name='chicken-history-retrieve-update-destroy'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
