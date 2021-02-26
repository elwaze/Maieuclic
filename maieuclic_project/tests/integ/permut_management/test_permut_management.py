from ..general_integ_tests import GeneralTestCase

from permut_management.models import Permut
from user.models import MaieuclicUser


class PermutManagementTestCase(GeneralTestCase):

    def setUp(self):
        super().setUp()
        self.permut = Permut.objects.create(users=[self.created_user.email])
        # Opening the link we want to test
        self.url = '{}/permut_management/my_permut'.format(self.live_server_url)
        self.selenium.get(self.url)

    def test_view_permuts_ok(self):
        # check the returned result
        self.assertIn('Mes permuts possibles', self.selenium.page_source)
        print(self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/permut_management/my_permut'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

    def test_view_permuts_change_permut_state(self):
        # find the form element
        permut_state = self.selenium.find_element_by_name("permut_state")
        change_permut_state = self.selenium.find_element_by_id("changepermutstate")
        # Fill the form with data
        permut_state.send_keys('UN')

        # submitting the form
        change_permut_state.click()
        # check the returned result
        self.assertIn('under negociation', self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/permut_management/my_permut'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

        # check that permut state is well saved in DB
        permut = Permut.objects.get(users=[self.created_user])
        self.assertEqual(permut.permut_state, 'UN')
        # check that user state changed in DB
        user_state = MaieuclicUser.objects.get(email=self.created_user.email).user_state
        self.assertFalse(user_state)
