from django.test import TestCase

from permut_creation.forms import PlaceForm


class TestPlaceForms(TestCase):
    """
    permut_creation app forms test.
    """

    def test_place_form_ok(self):
        """
        Tests if the user tries to create place left or searched.
        """
        data = {
            'city': 'La Tronche',
            'zipcode': '38700'
        }
        form = PlaceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_place_form_wrong_zipcode(self):
        data = {
            'city': 'La Tronche',
            'zipcode': '387001'
        }
        form = PlaceForm(data=data)
        self.assertFalse(form.is_valid())

    def test_place_form_wrong_city(self):
        data = {
            'city': 38700,
            'zipcode': '38700'
        }
        form = PlaceForm(data=data)
        self.assertFalse(form.is_valid())
