from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from permut_creation.forms import PlaceForm
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
            'zipcode': '38500'
        }
        Place.objects.create(
            city=self.left_place['city'],
            zipcode=self.left_place['zipcode']
        )
        self.searched_place = {
            'city': 'La Tronche',
            'zipcode': '38700',
        }
        Place.objects.create(
            city=self.searched_place['city'],
            zipcode=self.searched_place['zipcode'],
        )

    def test_place_form(self):
        """
        Tests if the user tries to create place left or searched.
        """
        data = {
            'city': self.left_place['city'],
            'zipcode': self.left_place['zipcode']
        }
        form = PlaceForm(data=data)
        self.assertTrue(form.is_valid())

    # def test_search_place_form(self):
    #     """
    #     Tests if the user tries to create searched place.
    #     """
    #     data = {
    #         'city': self.searched_place['city'],
    #         'zipcode': self.searched_place['zipcode']
    #     }
    #     form = PlaceForm(data=data)
    #     self.assertTrue(form.is_valid())
