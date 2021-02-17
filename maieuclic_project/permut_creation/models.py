from django.db import models
from django.core.validators import MinLengthValidator

# from user.models import MaieuclicUser

# Create your models here.


class PlaceManager(models.Manager):
    def create_place(self, city, zipcode):
        self.get_or_create(
            city=city,
            zipcode=zipcode,
        )


class Place(models.Model):

    class Meta:
        unique_together = ('city', 'zipcode')

    objects = PlaceManager()

    place_id = models.AutoField(primary_key=True)
    city = models.CharField('Ville', max_length=50)
    zipcode = models.CharField('Code Postal', max_length=5, validators=[MinLengthValidator(5)])
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)


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
    email = models.ForeignKey('user.MaieuclicUser', on_delete=models.CASCADE)
