from django.urls import path
from . import views

urlpatterns = [
    path('py_permut', views.my_permut, name='my_permut'),
]
