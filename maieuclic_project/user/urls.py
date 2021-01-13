from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^signin$', views.signin, name='signin'),
    re_path(r'^signout$', views.signout, name='signout'),
    re_path(r'^signup$', views.signup, name='signup'),
    re_path(r'^my_account$', views.my_account, name='my_account')
]
