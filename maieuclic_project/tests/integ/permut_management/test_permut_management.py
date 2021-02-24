from ..general_integ_tests import GeneralTestCase


class PermutManagementTestCase(GeneralTestCase):

    def setUp(self):
        super().setUp()
        # Opening the link we want to test
        self.url = '{}/permut_management/my_permut'.format(self.live_server_url)
        self.selenium.get(self.url)

    def test_view_permuts_ok(self):
        # check the returned result
        self.assertIn('Mes permuts possibles', self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/permut_management/my_permut'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
