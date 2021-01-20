from django.core import mail
from ..general_integ_tests import GeneralTestCase


class CoreTestCase(GeneralTestCase):
    login_required = False

    def setUp(self):
        super().setUp()

        self.home_url = '{}/home'.format(self.live_server_url)
        self.legals_url = '{}/home/legal_notices'.format(self.live_server_url)
        self.contact_url = '{}/home/contact'.format(self.live_server_url)
        self.sender = "selenium@gmail.com"
        self.subject_filling = "test"

    def test_home(self):
        self.selenium.get(self.home_url)
        # check the returned result
        self.assertIn(
            'Trouvez une mutation en quelques clics.',
            self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            self.home_url.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

    def test_legals(self):
        self.selenium.get(self.legals_url)
        # check the returned result
        self.assertIn(
            'MENTIONS',
            self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            self.legals_url.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

    def contact_basis(self, copy, subject_filling=""):
        self.selenium.get(self.contact_url)
        # Find the form element
        subject = self.selenium.find_element_by_name("subject")
        message = self.selenium.find_element_by_name("message")
        sender = self.selenium.find_element_by_name("sender")
        send_copy = self.selenium.find_element_by_name("send_copy")

        submit = self.selenium.find_element_by_xpath('//button[@type="submit"]')

        # Fill the form with data
        subject.send_keys(subject_filling)
        message.send_keys("message")
        sender.send_keys(self.sender)
        if copy:
            send_copy.click()

        # submitting the form
        submit.click()

    def test_contact_ok_copy(self):
        """
        Tests the contact form sends email to maieuclic with valid values.
        """
        copy = True
        self.contact_basis(copy, subject_filling=self.subject_filling)

        # check the returned result
        self.assertIn(
            'Votre message a bien été envoyé !',
            self.selenium.page_source)
        # check the e-mail have been sent
        self.assertEqual(len(mail.outbox), 1)

        # check the email content
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(len(mail.outbox[0].recipients()), 2)
        self.assertEqual(mail.outbox[0].recipients()[0], 'maieuclic@gmail.com')
        self.assertEqual(mail.outbox[0].recipients()[1], self.sender)
        self.assertIn('message', mail.outbox[0].body)

    def test_contact_no_copy(self):
        """
        Tests the contact form sends email to maieuclic with valid values.
        """
        copy = False
        self.contact_basis(copy, subject_filling=self.subject_filling)

        # check the returned result
        self.assertIn(
            'Votre message a bien été envoyé !',
            self.selenium.page_source)
        # check the e-mail have been sent
        self.assertEqual(len(mail.outbox), 1)

        # check the email content
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].recipients()[0], 'maieuclic@gmail.com')
        self.assertIn('message', mail.outbox[0].body)

    def test_contact_missing_field(self):
        """
        Tests the contact form with empty subject.
        """
        copy = False
        self.contact_basis(copy)

        # check the returned result
        self.assertNotIn(
            'Votre message a bien été envoyé !',
            self.selenium.page_source)
        # check the e-mail have not been sent
        self.assertEqual(len(mail.outbox), 0)
