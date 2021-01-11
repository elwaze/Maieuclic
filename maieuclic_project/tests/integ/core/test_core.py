from django.core import mail
from ..general_integ_tests import GeneralTestCase


class CoreTestCase(GeneralTestCase):
    login_required = False

    def setUp(self):
        super().setUp()

        self.contact_url = '{}/home/contact'.format(self.live_server_url)

    def core_basis(self, url):
        # Opening the link we want to test
        self.selenium.get(url)

    def test_contact(self):
        """
        Tests the contact form sends email to maieuclic.
        """
        # Find the form element
        subject = self.selenium.find_element_by_id("id_subject")
        message = self.selenium.find_element_by_name("message")
        sender = self.selenium.find_element_by_name("sender")
        send_copy = self.selenium.find_element_by_name("send_copy")

        submit = self.selenium.find_element_by_xpath('//button[@type="submit"]')

        # Fill the form with data
        subject.send_keys("test")
        message.send_keys("message")
        sender.send_keys("selenium@gmail.com")
        send_copy.send_keys(False)

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn(
            'Votre message a bien été envoyé !',
            self.selenium.page_source)
        # check the e-mail have been sent
        self.assertEqual(len(mail.outbox), 1)

        # check the email content
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].recipients()[0], 'selenium@gmail.com')
        self.assertIn('message', mail.outbox[0].body)
