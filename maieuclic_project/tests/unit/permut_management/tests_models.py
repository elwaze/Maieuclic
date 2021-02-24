from django.test import TestCase

from permut_management.models import Permut, UserPermutAssociation


class TestPermuts(TestCase):
    """Tests permuts creation in DB."""
    def setUp(self):
        self.users = []
        for user in textfixtures["users"]:
            self.users.append(user["email"])
        # get users from json fixture
        self.permut = Permut.objects.create(users=self.users)

    def test_permut_objects(self):
        self.assertIsInstance(Permut.objects)

    def test_permut_columns(self):
        permut = Permut.objects.get(users=self.users)
        self.assertEqual(self.users, permut.users)
        self.assertEqual("CR", permut.permut_state)
        self.assertIsInstance(permut.date_last_change)
        self.assertIsInstance(permut.date_time)
        self.assertEqual(permut.date_time, permut.date_last_change)
        self.assertIsInstance(permut.permut_id)


class TestUserPermutAssociation(TestCase):
    """Tests user-permut associations creation in DB."""
    def setUp(self):
        self.email_s = xxx
        self.permut_id = xxx
        self.place_id = xxx
        self.email = xxx
        self.assoc = UserPermutAssociation.objects.create(
            email=self.email,
            email_s=self.email_s,
            place_id=self.place_id,
            permut_id=self.permut_id
        )

    def test_user_permut_assoc_objects(self):
        self.assertIsInstance(UserPermutAssociation.objects)

    def test_user_permut_assoc_columns(self):
        assoc = UserPermutAssociation.objects.get(xxx)
        self.assertEqual(assoc.email_s, self.email_s)
        self.assertEqual(assoc.email, self.email)
        self.assertEqual(assoc.permut_id, self.permut_id)
        self.assertEqual(assoc.place_id, self.place_id)
