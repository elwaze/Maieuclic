from django.test import TestCase, Client
from django.urls import reverse

from user.models import MaieuclicUser


class TestPermutManagementViews(TestCase):
    def setUp(self):
        self.email = 'test@gmail.com'
        self.password = 'test'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        self.user.is_active = True
        self.user.save()

    def test_my_permut(self):
        """
        Getting the search_place url should return a http code = 200.
        """
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('my_permut'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='maieuclic_project/my_permut.html')
