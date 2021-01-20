from django.test import TestCase
from django.urls import reverse


class TestCore(TestCase):
    """
    Home app views test.
    """

    def test_home(self):
        """
        Getting the home page should return a http code = 200.
        """

        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/home.html')

    def test_legal(self):
        """
        Getting the legal notice page should return a http code = 200.
        """

        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/legal_notices.html')

    def test_contact(self):
        """
        Getting the contact page should return a http code = 200.
        """

        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/contact.html')
