from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from permut_creation.forms import PlaceLeftForm, PlaceSearchedForm
from permut_creation.models import Place, PermutSearch
from user.models import MaieuclicUser


class TestPlaceForms(TestCase):
    """
    permut_creation app forms test.
    """

    def setUp(self):
        self.email = 'moi@gmail.com'
        self.password = 'moi'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        self.left_place = {
            'city': 'Voiron',
            'zipcode': '38500',
            'hospital_name': "Centre Hospitalier de Voiron",
            'lat': 45.36939719281337,
            'lng': 5.595415411643872
        }
        Place.objects.create(
            city=self.left_place['city'],
            zipcode=self.left_place['zipcode'],
            hospital_name=self.left_place['hospital_name'],
            lat=self.left_place['lat'],
            lng=self.left_place['lng']
        )
        self.searched_place = {
            'city': 'La Tronche',
            'zipcode': '38700',
        }
        Place.objects.create(
            city=self.searched_place['city'],
            zipcode=self.searched_place['zipcode'],
        )

    def test_leave_place_form(self):
        """
        Tests if the user tries to create place left.
        """
        data = {
            'city': self.left_place['city'],
            'zipcode': self.left_place['zipcode']
        }
        form = PlaceLeftForm(data=data)
        # what should I check now ?

    def test_search_place_form(self):
        """
        Tests if the user tries to create searched place.
        """
        data = {
            'city': self.searched_place['city'],
            'zipcode': self.searched_place['zipcode']
        }
        form = PlaceSearchedForm(data=data)
        # what should I check now ?