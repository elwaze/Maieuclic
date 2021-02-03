from django.db import models
from django.core.validators import MinLengthValidator

from ..user.models import MaieuclicUser

# Create your models here.


class PlaceManager(models.Manager):
    def create_place(self, city, zipcode, hospital_name):
        self.get_or_create(
            city=city,
            zipcode=zipcode,
            hospital_name=hospital_name
        )


class Place(models.Model):

    class Meta:
        unique_together = ('city', 'zipcode', 'hospital_name')

    objects = PlaceManager()

    city = models.CharField('Ville')
    zipcode = models.CharField('Code Postal', max_length=5, validators=[MinLengthValidator(5)])
    hospital_name = models.CharField('Hôpital')
    lat = models.FloatField()
    lng = models.FloatField()


class PermutSearchManager(models.Manager):
    def save_searched_place(self, place_id, email):
        # si pas de place_id, creer une place ?
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
