from ..general_integ_tests import GeneralTestCase


class PermutCreationTestCase(GeneralTestCase):

    def setUp(self):
        super().setUp()
        # Opening the link we want to test
        self.url = '{}/permut_creation/permut_search'.format(self.live_server_url)
        self.selenium.get(self.url)

    def test_leave_place_ok(self):
        # find the form element
        city = self.selenium.find_element_by_name("city")
        zipcode = self.selenium.find_element_by_name("zipcode")
        save_left_place = self.selenium.find_element_by_id("save_left_place")
        save_searched_place = self.selenium.find_element_by_id("save_searched_place")
        # Fill the form with data
        city.send_keys('Voiron')
        zipcode.send_keys('38500')

        # submitting the form
        save_left_place.click()
        # check the returned result

    def test_searched_place_ok(self):
        # a modifier
        # find the form element
        city = self.selenium.find_element_by_name("city")
        zipcode = self.selenium.find_element_by_name("zipcode")
        save_left_place = self.selenium.find_element_by_id("save_left_place")
        save_searched_place = self.selenium.find_element_by_id("save_searched_place")
        # Fill the form with data
        city.send_keys('Voiron')
        zipcode.send_keys('38500')

        # submitting the form
        save_left_place.click()
        # check the returned result
