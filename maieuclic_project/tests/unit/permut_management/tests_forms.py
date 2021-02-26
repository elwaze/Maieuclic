from django.test import TestCase

from permut_management.forms import PermutStateForm


class TestPermutStateForm(TestCase):
    """
    permut_management app forms test.
    """

    def test_permut_state_form_ok(self):
        data = {'permut_state': 'BD'}
        form = PermutStateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_permut_state_form_wrong_value(self):
        data = {'permut_state': 'error'}
        form = PermutStateForm(data=data)
        self.assertFalse(form.is_valid())
