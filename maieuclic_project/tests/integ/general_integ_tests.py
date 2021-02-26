import os
import json

# from tests import TESTS_ROOT

from django.test import LiveServerTestCase
from user.models import MaieuclicUser
from permut_management.models import Permut, UserPermutAssociation
from permuct_creation.models import Place

from selenium import webdriver
from seleniumlogin import force_login
from webdriver_manager.chrome import ChromeDriverManager


PASSWORD = 'connection'
FIRST_NAME = 'Selenium'
EMAIL = 'selenium@gmail.com'


class GeneralTestCase(LiveServerTestCase):
    """
    Parent class to setup the selenium tests.
    """
    selenium = None
    created_user = None
    login_required = True

    def setUp(self) -> None:
        self.setup_fixtures()
        if self.login_required:
            force_login(self.created_user, self.selenium, self.live_server_url)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setup_selenium_driver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def setup_fixtures(cls):
        cls.created_user = MaieuclicUser.objects.create_superuser(
            email=EMAIL, password=PASSWORD
        )
        cls.permut = Permut.objects.create(users=[cls.created_user.email])
        cls.place = Place.objects.create(city='VOIRON', zipcode='38500')
        cls.user_permut_assoc = UserPermutAssociation.objects.create(
            permut_id=cls.permut,
            email=cls.created_user,
            email_s=cls.created_user,
            place_id=cls.place
        )

    @classmethod
    def setup_selenium_driver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1480")
        options.add_argument("disable-infobars")
        options.add_argument("disable-extensions")
        options.add_argument("headless")

        cls.selenium = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        cls.selenium.implicitly_wait(3)
