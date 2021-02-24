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
        print('looking for permutations')

        # creating graph
        graph = self.create_graph()
        # searching paths in the graph
        permuts = []
        for node in graph:
            permuts.append(self.find_permuts(graph, node, node))
        # # saving permutations
        print('total permuts')
        print(permuts)
        for permut in permuts:
            if permut != []:
                self.save_permut(permut)
        # # sending emails to people involved in new permutations
        # for permut in newpermuts:
        #     self.send_email(permut)

        self.logger.info('permutations successfully saved', exc_info=True)
        self.stdout.write(self.style.SUCCESS('permutations successfully saved'))
        print('permutations successfully saved')

    def create_graph(self):
        print('in create graph')
        graph = {}

        # get the users with user.user_state = True (a 1 place_id et n'est pas impliqué dans une permut en cours) and with at least 1 place searched
        users = MaieuclicUser.objects.filter(user_state=True)
        for user in users:
            print('user')
            print(user)
            node = (user.email, user.place_id.place_id)
            graph[node] = []
            search = PermutSearch.objects.filter(email=user)
            # garder les searches pour lesquelles il y a un giver != user
            for element in search:
                givers = MaieuclicUser.objects.filter(place_id__exact=element.place_id.place_id, user_state=True)
                for giver in givers:
                    graph[node].append((giver.email, giver.place_id.place_id))
            # dans le node on met le giver pas le searcher
            # for element in search:
            #     graph[node].append((element.place_id.place_id, element.email.email))
            if graph[node] == []:
                graph.pop(node)
        print(graph)
        return graph

    def find_permuts(self, graph, start, end, path=None):
        print('in find_permuts')
        if path is None:
            path = []
        path = path + [start]
        if start == end and len(path) != 1:
            return path
        permuts = []
        for node in graph[start]:
            print('node')
            print(node)
            if (node not in path) or (node == end):
                newpaths = self.find_permuts(graph, node, end, path=path)
                for newpath in newpaths:
                    permuts.append(newpath)
        print('permuts')
        print(permuts)
        return permuts

    def save_permut(self, permut):
        print('permut to be saved')
        print(permut)
        users = []
        for node in permut:
            users.append(node[0])
        print('users')
        print(users)
        permut_found = Permut.objects.filter(users__contains=users)
        print(permut_found)
        if not permut_found:
            print('no permut found')
            # save permut
            created_permut = Permut.objects.create(users=users)
            print(created_permut)
            # send email to people involved in permutation
            self.send_email(permut)
            # save associations between permut, user_s, place, user
            index = 0
            for element in permut:
                index += 1
                if index == len(permut):
                    index = -1
                print(index)
                user_s = MaieuclicUser.objects.get(email=element[0])
                print('user_s')
                print(user_s)
                user = MaieuclicUser.objects.get(email=permut[index][0])
                print(user)
                print('user')
                place = Place.objects.get(place_id=permut[index][1])
                print(place)
                print('place')
                UserPermutAssociation.objects.create(
                    email_s=user_s,
                    permut_id=created_permut,
                    place_id=place,
                    email=user
                )

    def send_email(self, permut):
        # a la fin, passer la permut a notified
        pass
