from django.db import models
from django.core.validators import MinLengthValidator

from user.models import MaieuclicUser

# Create your models here.


class PlaceManager(models.Manager):
    pass


class Place(models.Model):
    city = models.CharField('Ville')
    zipcode = models.CharField('Code Postal', max_length=5, validators=[MinLengthValidator(5)])
    hospital_name = models.CharField('hôpital')
    lat = models.FloatField()
    lng = models.FloatField()


class PermutSearchManager(models.Manager):
    def save_searched_place(self, place_id, email):
        self.get_or_create(
            place_id=place_id,
            email=email
        )


class PermutSearch(models.Model):

    class Meta:
        unique_together = ('place_id', 'email')

    objects = PermutSearchManager()
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    email = models.ForeignKey(MaieuclicUser, on_delete=models.CASCADE)




