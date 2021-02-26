import json
from django.test import TestCase

from permut_management.models import Permut, UserPermutAssociation
from permut_creation.models import Place
from user.models import MaieuclicUser


class TestPermuts(TestCase):
    """Tests permuts creation in DB."""
    def setUp(self):
        self.users = []
        with open('maieuclic_project/tests/test_fixtures.json') as fd:
            fixtures = json.load(fd)
        for user in fixtures["users"]:
            self.users.append(user["email"])
        # get users from json fixture
        self.permut = Permut.objects.create(users=self.users)
        print('self.permut1')
        print(self.permut)

    def test_permut_objects(self):
        self.assertIsInstance(self.permut, Permut.objects)

    def test_permut_columns(self):
        permut = Permut.objects.get(users=self.users)
        self.assertEqual(self.users, permut.users)
        self.assertEqual("CR", permut.permut_state)
        # self.assertIsInstance(permut.date_last_change, Permut)
        # self.assertIsInstance(permut.date_time, Permut)
        self.assertEqual(permut.date_time, permut.date_last_change)
        # self.assertIsInstance(permut.permut_id, Permut)


class TestUserPermutAssociation(TestCase):
    """Tests user-permut associations creation in DB."""
    def setUp(self):
        # get users from json fixture
        self.users = []

        with open('maieuclic_project/tests/test_fixtures.json') as fd:
            fixtures = json.load(fd)
            places = []
            index = 0
        for place in fixtures["places"]:
            new_place = Place.objects.create(city=place["city"], zipcode=place["zipcode"])
            print("new_place")
            print(new_place)
            places.append(new_place)
        # get users from json fixture
        for user in fixtures["users"]:
            print("user")
            print(user)
            new_user = MaieuclicUser.objects.create(
                email=user["email"],
                password=user["password"],
                user_state=True,
                place_id=places[index],
                is_active=True
            )
            print("new_user")
            print(new_user)

            self.users.append(user["email"])
            index += 1

        print("users")
        print(self.users)
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
        print("self.assoc")
        print(self.assoc)
        print(self.assoc.email_s)
        print(self.assoc.email)
        print(self.assoc.permut_id)
        print(self.assoc.place_id)

    def test_user_permut_assoc_objects(self):
        self.assertIsInstance(self.assoc, UserPermutAssociation.objects)

    def test_user_permut_assoc_columns(self):
        assoc = UserPermutAssociation.objects.get(id=self.assoc)
        self.assertEqual(assoc.email_s, self.email_s)
        self.assertEqual(assoc.email, self.email)
        self.assertEqual(assoc.permut_id, self.permut_id)
        self.assertEqual(assoc.place_id, self.place_id)
