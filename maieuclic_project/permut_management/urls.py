from django.urls import path
from . import views

urlpatterns = [
    path('my_permut', views.my_permut, name='my_permut'),
]
