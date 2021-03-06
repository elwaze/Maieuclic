from django.test import TestCase, Client
from user.models import MaieuclicUser
from user.tokens import account_activation_token

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class TestUserViews(TestCase):
    """
    User app views test.
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.password = 'test'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        self.user.is_active = False
        self.user.save()
        self.token = account_activation_token.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))

    def test_user_connection_page(self):
        """
        Getting the connection page should return a http code = 200.
        """

        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='maieuclic_project/signin.html')

    def test_user_signin(self):
        """
        The connection with valid information should return a http code = 200.
        """

        response = self.client.post(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='user/signin.html')

    def test_user_my_account(self):
        """
        Getting the user's account page when the user is connected should return a http code = 200.
        """
        self.user.is_active = True
        self.user.save()
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='user/my_account.html')

    def test_user_signgout(self):
        """
        Signing out should return a http code = 200. and redirect to home page.
        """
        self.user.is_active = True
        self.user.save()
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='core/home.html')

    def test_user_signup(self):
        """
        Getting the signup page should return a http code = 200.
        """

        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='user/signup.html')

    def test_activate(self):
        """
        calling activate should return a http code = 302.
        after that, the user should be activated.
        """
        response = self.client.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        self.assertEqual(response.status_code, 302)
        user = MaieuclicUser.objects.get(pk=self.user.pk)
        self.assertEqual(user.is_active, True)
        self.assertTemplateUsed(template_name='user/my_account.html')

    # def test_user_delete_account(self):
    #     self.client.login(email=self.email, password=self.password)
    #     response = self.client.get(reverse('delete_account'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(template_name='core/home.html')
