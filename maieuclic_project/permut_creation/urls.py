from django.urls import path
from . import views

urlpatterns = [
    path('permut_search', views.permut_search, name='permut_search'),
]
