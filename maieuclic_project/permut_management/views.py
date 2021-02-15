from django.shortcuts import render

# Create your views here.


def my_permut(request):
    # recuperer les permuts assoc a l'utilisateur
    # afficher la liste des permuts : poste a recuperer, etat de la permut, coord de la personne qui donne ce poste si auth ok, coord de la personne a qui l'user donne son poste si auth ok
    # possibilite de changer l'etat de la permut.
    # si etat passe a BD ou UN, passer tous les user_state a false.
    # si etat permut passe a RE, repasser tous les user_state a true
    pass
