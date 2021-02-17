from django.urls import path
from . import views

urlpatterns = [
    path('permut_search', views.permut_creation, name='permut_search'),
]
