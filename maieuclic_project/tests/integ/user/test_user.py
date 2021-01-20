from maieuclic_project.tests.integ.general_integ_tests import EMAIL, PASSWORD
from maieuclic_project.tests.integ.general_integ_tests import GeneralTestCase

from django.core import mail
import re


class AccountTestCase(GeneralTestCase):
    login_required = False

    def setUp(self):
        super().setUp()

        self.signup_url = '{}/user/signup?'.format(self.live_server_url)
        self.signin_url = '{}/user/signin'.format(self.live_server_url)

    def account_basis(self, url):
        """
        Common settings depending on the page we want (signup or signin).

        :param url: url of the page we want.
        :return email, password, pwd_confirm, submit: form elements found.
        when using signin url, pwd_confirm not found
        -> replaced by an empty string.
        """
        # Opening the link we want to test
        self.selenium.get(url)

        # find the form element
        email = self.selenium.find_element_by_name("email")
        password = self.selenium.find_element_by_name("password")
        try:
            pwd_confirm = self.selenium.find_element_by_name("pwd_confirm")
        except:
            pwd_confirm = ""

        submit = self.selenium.find_element_by_xpath('//input[@type="submit"]')

        return email, password, pwd_confirm, submit

    def test_signup_ok(self):
        """
        Tests the user account creation with a valid form.
        """
        email, password, pwd_confirm, submit = self.account_basis(self.signup_url)
        # Fill the form with data
        email.send_keys('created.{}'.format(EMAIL))
        password.send_keys('created_{}'.format(PASSWORD))
        pwd_confirm.send_keys('created_{}'.format(PASSWORD))

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn(
            'Veuillez confirmer votre adresse email pour valider la création de votre compte Maieuclic',
            self.selenium.page_source)
        # check the e-mail have been sent
        self.assertEqual(len(mail.outbox), 1)

        # check the email content
        self.assertEqual(mail.outbox[0].subject, 'Finalisez la création de votre compte Maieuclic')
        self.assertEqual(mail.outbox[0].recipients()[0], 'created.{}'.format(EMAIL))
        self.assertIn('Pour confirmer la création de votre compte Maieuclic, veuillez cliquer sur le lien suivant :', mail.outbox[0].body)

        # check that the activation link works
        link = re.split(r'href="', mail.outbox[0].body)[1]
        link = re.split(r'">Je', link)[0]
        self.assertIn('/user/activate/', link)

    def test_signup_diff_pwd(self):
        """
        Tests the user account creation,
        when the confirmation password is different from the first password.
        """
        email, password, pwd_confirm, submit = self.account_basis(self.signup_url)

        # Fill the form with data
        email.send_keys('signup_diff_pwd@selenium.com')
        password.send_keys('signup_pwd')
        pwd_confirm.send_keys('signup_diff_pwd')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('veuillez entrer un mot de passe de confirmation identique', self.selenium.page_source)

    def test_signin_wrong_pwd(self):
        """
        Tests the user signin with a wrong password.
        """
        email, password, pwd_confirm, submit = self.account_basis(self.signin_url)

        # Fill the form with data
        email.send_keys(EMAIL)
        password.send_keys('signin_wrong_pwd')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Utilisateur inconnu ou mauvais de mot de passe.', self.selenium.page_source)

    def test_signin_user_not_known(self):
        """
        Tests the user signin with a wrong password.
        """
        email, password, pwd_confirm, submit = self.account_basis(self.signin_url)

        # Fill the form with data
        email.send_keys('user_not_known@test.com')
        password.send_keys('selenium_test')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Utilisateur inconnu ou mauvais de mot de passe.', self.selenium.page_source)

    def test_signin_ok(self):
        """
        Tests the user connection with a valid form.
        """
        email, password, pwd_confirm, submit = self.account_basis(self.signin_url)

        # Fill the form with data
        email.send_keys(EMAIL)
        password.send_keys(PASSWORD)

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Bonjour', self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/user/my_account'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

        # logout at the end of the test, not to be logged in for next test
        logout = self.selenium.find_element_by_xpath('//a[@href="/user/logout"]')
        logout.click()

    def test_change_my_account(self):
        pass

    def test_delete_account(self):
        pass
