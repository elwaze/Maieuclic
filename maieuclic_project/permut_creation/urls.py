from django.urls import path

from . import views

urlpatterns = [
    path('search_place', views.search_place, name='search_place'),
    path('leave_place', views.leave_place, name='leave_place'),
]
