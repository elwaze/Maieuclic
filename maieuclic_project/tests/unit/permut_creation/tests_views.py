from django.test import TestCase, Client
from django.urls import reverse

# from permut_creation.models import Place, PermutSearch
from user.models import MaieuclicUser


class TestPermutCreationViews(TestCase):
    """
    Permut_creation app views test.
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.password = 'test'
        self.client = Client()
        self.user = MaieuclicUser.objects.create_user(email=self.email, password=self.password)
        self.user.is_active = True
        self.user.save()

    def test_leave_place(self):
        """
        Getting the search_place url should return a http code = 200.
        """
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('search_place'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='maieuclic_project/permut_search.html')

    def test_search_place(self):
        """
        Getting the search_place url should return a http code = 200.
        """
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('leave_place'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='maieuclic_project/permut_search.html')
