from user.models import MaieuclicUser

from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from user.forms import SignupForm, SigninForm


class TestUserForms(TestCase):
    """
    User app forms test.
    """

    def setUp(self):
        self.email = 'moi@gmail.com'
        self.signup_email = 'newemail@gmail.com'
        self.password = 'moi'
        self.pwd_confirm = 'me'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        # self.data = {
        #     'email': self.email,
        #     'password': self.password,
        #     # 'pwd_confirm': self.pwd_confirm
        # }

    def test_user_wrong_email(self):
        """
        Tests if the user tries to signin to an account with not known email.
        """
        data = {
            'email': self.signup_email,
            'password': self.password
        }
        form = SigninForm(data=data)
        self.assertRaises(ValidationError, form.clean_email)
        # with self.assertRaises(ValidationError):
        #     form = SigninForm(data=data)

    def test_user_wrong_pwd(self):
        """
        Tests if the user tries to signin to an account with a wrong password.
        """
        data = {
            'email': self.email,
            'password': self.pwd_confirm
        }
        form = SigninForm(data=data)
        self.assertRaises(ValidationError, form.clean_password)
        # with self.assertRaises(ValidationError):
        #     form = SigninForm(data=data)

    def test_user_valid_signinform(self):
        """
        Tests if the user tries to signin to an account with valid values.
        """
        # data = self.data
        # data['pwd_confirm'] = data['password']
        data = {
            'email': self.email,
            'password': self.password
        }
        form = SigninForm(data=data)

        self.assertTrue(form.is_valid())

    def test_user_signupform_same_email(self):
        """
        Tests if the user tries to create an account with an already used username.
        """
        data = {
            'email': self.email,
            'password': self.password,
            'pwd_confirm': self.password
        }
        form = SignupForm(data=data)
        self.assertRaises(ValidationError, form.clean_email)

    def test_user_signupform_wrong_confirm_pwd(self):
        """
        Tests if the confirmation password is different from the first password.
        """
        data = {
            'email': self.email,
            'password': self.password,
            'pwd_confirm': self.pwd_confirm
        }
        form = SignupForm(data=data)
        self.assertRaises(ValidationError, form.clean_pwd_confirm)

    def test_user_valid_signupform(self):
        """
        Tests if the user tries to create an account with valid values.
        """
        data = {
            'email': self.signup_email,
            'password': self.password,
            'pwd_confirm': self.password
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.signup_email, form.clean_email())
        self.assertEqual(self.password, form.clean_pwd_confirm())
