from django.urls import path
from . import views

urlpatterns = [
    # path('permut_search', views.permut_creation, name='permut_search'),
    path('search_place', views.search_place, name='search_place'),
    path('leave_place', views.leave_place, name='leave_place'),
]
