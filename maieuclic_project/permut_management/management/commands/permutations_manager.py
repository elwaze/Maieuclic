#!/usr/bin/env python3
"""
Running a path finder to search possible permutations,
save new permutations in DB and send notification email to the involved people.
"""
import logging

from django.core.management.base import BaseCommand
from user.models import MaieuclicUser
from permut_creation.models import PermutSearch
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
        print('looking for permutations')

        # creating graph
        graph = self.create_graph()
        # searching paths in the graph
        permuts = []
        for node in graph:
            permuts.append(self.find_permuts(graph, node, node))
        # # saving permutations
        for permut in permuts:
            self.save_permut(permut)
        # # sending emails to people involved in new permutations
        # for permut in newpermuts:
        #     self.send_email(permut)

        self.logger.info('permutations successfully saved', exc_info=True)
        self.stdout.write(self.style.SUCCESS('permutations successfully saved'))
        print('permutations successfully saved')

    def create_graph(self):
        graph = {}

        # get the users with user.user_state = True (a 1 place_id et n'est pas impliqué dans une permut en cours) and with at least 1 place searched
        users = MaieuclicUser.objects.filter(user_state=True)
        for user in users:
            node = (user.email, user.place_id)
            graph[node] = []
            search = PermutSearch.objects.filter(email=user.email)
            for element in search:
                graph[node].append((element.place_id, element.email))
            if graph[node] == []:
                graph.pop(node)

        return graph

    def find_permuts(self, graph, start, end, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start == end and len(path) != 1:
            return path
        permuts = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_permuts(graph, node, end, path)
                for newpath in newpaths:
                    permuts.append(newpath)
        return permuts

    def save_permut(self, permut):
        users = set()
        for node in permut:
            print(node)
            users = users + node[1]

        permut_found = Permut.objects.filter(users__contains=users)
        print(permut_found)
        if permut_found : # ya un truc a arranger la
            pass
        else:
            # enreg la permut
            created_permut = Permut.objects.create(users=users)
            # send email to people involved in permutation
            self.send_email(permut)
            # save associations between permut, user_s, place, user
            index = 0
            for element in permut:
                index += 1
                user_s = element[1]
                user = permut[index - 2][1]
                place = element[0]
                linked_permut = created_permut.pk
                UserPermutAssociation.objects.create(
                    email_s=user_s,
                    permut_id=linked_permut,
                    place_id=place,
                    email=user
                )

    def send_email(self, permut):
        # a la fin, passer la permut a notified
        pass
