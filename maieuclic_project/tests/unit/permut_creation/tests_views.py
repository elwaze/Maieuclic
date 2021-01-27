from django.test import TestCase, Client
from django.urls import reverse

from permut_creation.models import Place, PermutSearch


class TestPermutCreationViews(TestCase):
    """
    Permut_creation app views test.
    """

    def setUp(self):
        pass

    def test_permut_search_page(self):
        """
        Getting the permut_search page should return a http code = 200.
        """

        response = self.client.get(reverse('permut_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='maieuclic_project/permut_search.html')
        # y a des trucs a rajouter...
