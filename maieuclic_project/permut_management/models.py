from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models import MaieuclicUser
from permut_creation.models import Place


# Create your models here.


class Permut(models.Model):
    states = [('CR', 'created'), ('NO', 'notified'), ('BD', 'being discussed'), ('UN', 'under negociation'), ('RE', 'rejected')]
    permut_id = models.AutoField(primary_key=True)
    permut_state = models.CharField(choices=states, default='CR', max_length=2)
    date_last_change = models.DateTimeField(auto_now=True)
    users = ArrayField(models.EmailField())
    date_time = models.DateTimeField(auto_now_add=True)


class UserPermutAssociation(models.Model):
    email_s = models.ForeignKey(MaieuclicUser, related_name='user_searching_this_place', on_delete=models.CASCADE)
    permut_id = models.ForeignKey(Permut, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    email = models.ForeignKey(MaieuclicUser, related_name='user_leaving_this_place', on_delete=models.CASCADE)
