import json
from django.test import TestCase

from permut_management.models import Permut, UserPermutAssociation
from permut_creation.models import Place
from user.models import MaieuclicUser


class TestPermuts(TestCase):
    """Tests permuts creation in DB."""
    def setUp(self):
        # get users from json fixture
        self.users = []
        with open('maieuclic_project/tests/test_fixtures.json') as fd:
            fixtures = json.load(fd)
        for user in fixtures["users"]:
            self.users.append(user["email"])
        self.permut = Permut.objects.create(users=self.users)

    def test_permut_objects(self):
        self.assertIsInstance(self.permut, Permut)

    def test_permut_columns(self):
        permut = Permut.objects.get(users=self.users)
        self.assertEqual(self.users, permut.users)
        self.assertEqual("CR", permut.permut_state)
        self.assertIsNotNone(permut.date_last_change)
        self.assertIsNotNone(permut.date_time)
        self.assertIsNotNone(permut.permut_id)


class TestUserPermutAssociation(TestCase):
    """Tests user-permut associations creation in DB."""
    def setUp(self):
        self.users = []
        with open('maieuclic_project/tests/test_fixtures.json') as fd:
            fixtures = json.load(fd)
            places = []
            index = 0
        # create places from json fixture
        for place in fixtures["places"]:
            new_place = Place.objects.create(city=place["city"], zipcode=place["zipcode"])
            places.append(new_place)
        # create users from json fixture
        for user in fixtures["users"]:
            new_user = MaieuclicUser.objects.create(
                email=user["email"],
                password=user["password"],
                user_state=True,
                place_id=places[index],
                is_active=True
            )

            self.users.append(new_user)
            index += 1

        self.permut_id = Permut.objects.create(users=self.users)
        self.email_s = self.users[0]
        self.place_id = places[1]
        self.email = self.users[1]
        self.assoc = UserPermutAssociation.objects.create(
            email=self.email,
            email_s=self.email_s,
            place_id=self.place_id,
            permut_id=self.permut_id
        )

    def test_user_permut_assoc_objects(self):
        self.assertIsInstance(self.assoc, UserPermutAssociation)

    def test_user_permut_assoc_columns(self):
        assoc = UserPermutAssociation.objects.get(id=self.assoc.id)
        self.assertEqual(assoc.email_s, self.email_s)
        self.assertEqual(assoc.email, self.email)
        self.assertEqual(assoc.permut_id, self.permut_id)
        self.assertEqual(assoc.place_id, self.place_id)
