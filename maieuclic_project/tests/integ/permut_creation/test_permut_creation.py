from ..general_integ_tests import GeneralTestCase

from permut_creation.models import Place, PermutSearch
from user.models import MaieuclicUser


class PermutCreationTestCase(GeneralTestCase):

    def setUp(self):
        super().setUp()
        # Opening the link we want to test
        self.url = '{}/permut_creation/leave_place'.format(self.live_server_url)
        self.selenium.get(self.url)

    def test_leave_place_ok(self):
        # find the form element
        city = self.selenium.find_element_by_name("leave-city")
        zipcode = self.selenium.find_element_by_name("leave-zipcode")
        save_left_place = self.selenium.find_element_by_id("save_place_left")
        # Fill the form with data
        city.send_keys('Voiron')
        zipcode.send_keys('38500')

        # submitting the form
        save_left_place.click()
        # check the returned result
        self.assertIn('38500', self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/permut_creation/leave_place'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        # check that left place is well saved in DB
        left_place = MaieuclicUser.objects.get(email=self.created_user.email).place_id
        self.assertEqual(left_place.city, 'VOIRON')
        self.assertEqual(left_place.zipcode, '38500')

    def test_searched_place_ok(self):
        # find the form element
        city = self.selenium.find_element_by_name("search-city")
        zipcode = self.selenium.find_element_by_name("search-zipcode")
        save_searched_place = self.selenium.find_element_by_id("save_place_searched")
        # Fill the form with data
        city.send_keys('Grenoble')
        zipcode.send_keys('38000')

        # submitting the form
        save_searched_place.click()
        # check the returned result
        self.assertIn('38000', self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/permut_creation/search_place'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        # check that searched place is saved in DB
        searched_place = PermutSearch.objects.get(email=self.created_user).place_id
        self.assertEqual(searched_place.city, 'GRENOBLE')
        self.assertEqual(searched_place.zipcode, '38000')
