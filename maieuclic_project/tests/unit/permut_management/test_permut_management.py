from django.test import TestCase
import unittest.mock as mock
from permut_management.management.commands.permutations_manager import Command
from user.models import MaieuclicUser
from permut_creation.models import PermutSearch, Place
from permut_management.models import Permut, UserPermutAssociation


class TestCommand(TestCase):
    def setUp(self):
        pass
        # self.command = Command()
        # self.user1 = {
        #     "email": "user1@maieuclic.com",
        #
        # }