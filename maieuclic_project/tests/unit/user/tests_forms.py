from user.models import MaieuclicUser

from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from user.forms import SignupForm


class TestUserForms(TestCase):
    """
    User app forms test.
    """

    def setUp(self):
        self.email = 'moi@gmail.com'
        self.password = 'moi'
        self.pwd_confirm = 'me'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        self.data = {
            'email': self.email,
            'password': self.password,
            'pwd_confirm': self.pwd_confirm
        }

    def test_user_valid_form(self):
        """
        Tests if the user tries to create an account with valid values.
        """
        data = self.data
        data['pwd_confirm'] = data['password']
        form = SignupForm(data=self.data)
        self.assertEqual(self.email, form.clean_email)
        self.assertEqual(self.pwd_confirm, form.clean_pwd_confirm)

    def test_user_form_same_email(self):
        """
        Tests if the user tries to create an account with an already used username.
        """
        form = SignupForm(data=self.data)
        self.assertRaises(ValidationError, form.clean_email)

    def test_user_form_wrong_confirm_pwd(self):
        """
        Tests if the confirmation password is different from the first password.
        """
        form = SignupForm(data=self.data)
        self.assertRaises(ValidationError, form.clean_pwd_confirm)
