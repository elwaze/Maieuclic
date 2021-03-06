from django.test import TestCase

from permut_creation.models import Place, PlaceManager, PermutSearch, PermutSearchManager
from user.models import MaieuclicUser


class GeneralTestPlace(TestCase):
    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "password"
        self.left_place = {
            'city': 'Voiron',
            'zipcode': '38500'
        }
        self.searched_place = {
            'city': 'La Tronche',
            'zipcode': '38700',
        }
        Place.objects.create(
            city=self.left_place['city'],
            zipcode=self.left_place['zipcode']
        )
        Place.objects.create(
            city=self.searched_place['city'],
            zipcode=self.searched_place['zipcode'],
        )
        MaieuclicUser.objects.create(
            email=self.email,
            password=self.password
        )


class TestPlace(GeneralTestPlace):
    """
    Tests the place creation in DB.
    """

    def test_place_objects(self):
        self.assertIsInstance(Place.objects, PlaceManager)

    def test_place_columns(self):
        place = Place.objects.get(city=self.left_place['city'])
        self.assertEqual(self.left_place['city'], place.city)
        self.assertEqual(self.left_place['zipcode'], place.zipcode)

    def test_place_associated_to_user(self):
        place = Place.objects.get(city=self.left_place['city'])
        MaieuclicUser.objects.save_place_left(self.email, place)
        user = MaieuclicUser.objects.get(email=self.email)
        self.assertEqual(user.place_id, place)


class TestPermutSearch(GeneralTestPlace):
    """
    Tests the permut_search creation in DB.
    """
    def setUp(self):
        GeneralTestPlace.setUp(self)
        self.user = MaieuclicUser.objects.get(email=self.email)
        self.place_id = Place.objects.get(city=self.searched_place['city'])
        self.model = PermutSearch.objects.save_searched_place(self.place_id, self.user)

    def test_permut_search_objects(self):
        self.assertIsInstance(PermutSearch.objects, PermutSearchManager)

    def test_permut_search_columns(self):
        permut_search = PermutSearch.objects.get(place_id=self.place_id, email=self.user)
        self.assertEqual(self.user, permut_search.email)
        self.assertEqual(self.place_id, permut_search.place_id)
