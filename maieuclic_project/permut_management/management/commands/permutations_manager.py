#!/usr/bin/env python3
"""
Running a path finder to search possible permutations,
save new permutations in DB and send notification email to the involved people.
"""
import logging

from django.core.management.base import BaseCommand

from user.models import MaieuclicUser
from permut_creation.models import PermutSearch, Place
from permut_management.models import Permut, UserPermutAssociation


class Command(BaseCommand):
    help = 'Search possible permutation between places and save it in DB.' \
           '\n If the permutation is new, send email to the involved people'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.testing = False
        self.logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.testing = options.get('testing')
        self.logger.info('looking for permutations', exc_info=True)
        self.stdout.write('looking for permutations')

        # creating graph
        graph = self.create_graph()

        # searching paths in the graph
        permuts = []
        for node in graph:
            permuts.append(self.find_permuts(graph, node, node))

        # # saving permutations
        nb_new_permuts = 0
        for permut in permuts:
            if permut != []:
                nb_new_permuts = self.save_permut(permut, nb_new_permuts)

        self.logger.info('permutations successfully saved', exc_info=True)
        self.stdout.write(self.style.SUCCESS('permutations successfully saved'))

    def create_graph(self):
        """
        Creates a graph whith all the plasses left and all the places searched.
        """
        graph = {}

        # get the users with user.user_state = True and with at least 1 place searched
        users = MaieuclicUser.objects.filter(user_state=True)
        for user in users:
            node = (user.email, user.place_id.place_id)
            graph[node] = []
            search = PermutSearch.objects.filter(email=user)
            # keeping searches where giver != user
            for element in search:
                givers = MaieuclicUser.objects.filter(place_id__exact=element.place_id.place_id, user_state=True)
                for giver in givers:
                    graph[node].append((giver.email, giver.place_id.place_id))
            if graph[node] == []:
                graph.pop(node)
        return graph

    def find_permuts(self, graph, start, end, path=None):
        """
        Walking threw the graph to find loop paths.
        """
        if path is None:
            path = []
        path = path + [start]
        if start == end and len(path) != 1:
            return path
        permuts = []
        for node in graph[start]:
            if (node not in path) or (node == end):
                newpaths = self.find_permuts(graph, node, end, path=path)
                for newpath in newpaths:
                    permuts.append(newpath)
        return permuts

    def save_permut(self, permut, nb_new_permuts):
        """
        Saving permut found if not already exists in DB.
        """
        users = []
        for node in permut:
            users.append(node[0])
        permut_found = Permut.objects.filter(users__contains=users)
        if not permut_found:

            # save permut
            created_permut = Permut.objects.create(users=users)
            nb_new_permuts += 1

            # send email to people involved in permutation
            # self.send_email(permut)

            # save associations between permut, user_s, place, user
            index = 0
            for element in permut:
                index += 1
                if index == len(permut):
                    index = -1
                user_s = MaieuclicUser.objects.get(email=element[0])

                user = MaieuclicUser.objects.get(email=permut[index][0])

                place = Place.objects.get(place_id=permut[index][1])

                UserPermutAssociation.objects.create(
                    email_s=user_s,
                    permut_id=created_permut,
                    place_id=place,
                    email=user
                )
        return nb_new_permuts

    # def send_email(self, permut):
    #     # a la fin, passer la permut a notified
    #     pass
