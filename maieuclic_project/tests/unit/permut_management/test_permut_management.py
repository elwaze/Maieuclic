import json

from django.test import TestCase
import unittest.mock as mock

from permut_management.management.commands.permutations_manager import Command
from user.models import MaieuclicUser
from permut_creation.models import PermutSearch, Place
from permut_management.models import Permut, UserPermutAssociation


class TestCommand(TestCase):
    def setUp(self):
        with open('maieuclic_project/tests/test_fixtures.json') as fd:
            fixtures = json.load(fd)
        self.places = []
        for place in fixtures['places']:
            place_created = Place.objects.create(city=place['city'], zipcode=place['zipcode'])
            self.places.append(place_created)
        self.emails = []
        for user in fixtures['users']:
            user_created = MaieuclicUser.objects.create(
                email=user['email'],
                password=['password'],
                place_id=self.places[user['place']]
            )
            user_created.user_state = True
            user_created.save()
            self.emails.append(user['email'])
            place_searched = PermutSearch.objects.create(place_id=self.places[user['place'] - 1], email=user_created)

        self.command = Command()
        self.expected_graph = {
            ('user1@maieuclic.com', self.places[0].place_id): [('user3@maieuclic.com', self.places[2].place_id)],
            ('user2@maieuclic.com', self.places[1].place_id): [('user1@maieuclic.com', self.places[0].place_id)],
            ('user3@maieuclic.com', self.places[2].place_id): [('user2@maieuclic.com', self.places[1].place_id)]
        }
        self.expected_permut = [
            ('user1@maieuclic.com', self.places[0].place_id),
            ('user3@maieuclic.com', self.places[2].place_id),
            ('user2@maieuclic.com', self.places[1].place_id),
            ('user1@maieuclic.com', self.places[0].place_id)
        ]

    def test_create_graph(self):
        # calling function
        graph = self.command.create_graph()

        # expected result
        self.assertEqual(graph, self.expected_graph)

    def test_find_permuts(self):
        # calling function
        for node in self.expected_graph:
            permuts_found = self.command.find_permuts(self.expected_graph, node, node)
            break

        # expected result
        self.assertEqual(permuts_found, self.expected_permut)

    def test_save_permut(self):
        permut_saved = 0
        permut_saved = self.command.save_permut(self.expected_permut, permut_saved)

        # expected result
        permut_found = Permut.objects.filter(users__contains=self.emails).count()
        self.assertEqual(permut_found, 1)
        self.assertEqual(permut_saved, 1)

        # case where the permut is already in DB
        permut_saved = 0
        permut_saved = self.command.save_permut(self.expected_permut, permut_saved)

        # expected result
        permut_found = Permut.objects.filter(users__contains=self.emails).count()
        self.assertEqual(permut_found, 1)
        self.assertEqual(permut_saved, 0)

    @mock.patch('permut_management.management.commands.permutations_manager.Command.create_graph')
    @mock.patch('permut_management.management.commands.permutations_manager.Command.find_permuts')
    @mock.patch('permut_management.management.commands.permutations_manager.Command.save_permut')
    def test_handle(self, mocked_save_permut, mocked_find_permuts, mocked_create_graph):

        # mocking
        mocked_create_graph.return_value = self.expected_graph
        mocked_find_permuts.return_value = self.expected_permut  # pb : il y a plus expected permuts
        mocked_save_permut.return_value = 1  # ??

        # calling function
        self.command.handle()

        # expected results
        mocked_create_graph.assert_called_once_with()
        mocked_find_permuts.assert_has_calls([
            mock.call(
                self.expected_graph,
                ('user1@maieuclic.com', self.places[0].place_id),
                ('user1@maieuclic.com', self.places[0].place_id)
            ),
            mock.call(
                self.expected_graph,
                ('user2@maieuclic.com', self.places[1].place_id),
                ('user2@maieuclic.com', self.places[1].place_id)
            ),
            mock.call(
                self.expected_graph,
                ('user3@maieuclic.com', self.places[2].place_id),
                ('user3@maieuclic.com', self.places[2].place_id)
            )
        ])
        mocked_save_permut.assert_has_calls([
            mock.call(self.expected_permut, 0),
            mock.call(self.expected_permut, 1),
            mock.call(self.expected_permut, 1)
        ])
