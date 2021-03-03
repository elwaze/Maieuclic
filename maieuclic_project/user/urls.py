from django.urls import path

from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup', views.signup, name='signup'),
    path('my_account', views.my_account, name='my_account'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('delete_account', views.delete_account, name='delete_account'),
]
