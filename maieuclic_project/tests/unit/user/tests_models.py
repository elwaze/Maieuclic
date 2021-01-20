from django.test import TestCase

from user.models import MaieuclicUser, MaieuclicUserManager


class TestUser(TestCase):
    """
    Tests user creation in DB.
    """

    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "password"
        self.user = MaieuclicUser.objects.create(email=self.email, password=self.password)

    def test_user_objects(self):
        self.assertIsInstance(MaieuclicUser.objects, MaieuclicUserManager)

    def test_user_columns(self):
        user = MaieuclicUser.objects.get(email=self.email)
        self.assertEqual(self.email, user.email)
        self.assertEqual(self.password, user.password)
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.phone_number, "")
        self.assertFalse(user.user_state)
        # self.assertIsNone(user.place_id)
        self.assertFalse(user.email_authorization)
        self.assertFalse(user.phone_authorization)
