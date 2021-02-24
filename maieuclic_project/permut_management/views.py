from django.shortcuts import render

from .forms import PermutStateForm
from .models import UserPermutAssociation, Permut
from permut_creation.models import Place
from user.models import MaieuclicUser

# Create your views here.


def my_permut(request):

    error = False
    user = request.user

    # get permuts associated to user
    permuts_assoc = UserPermutAssociation.objects.filter(email_s__exact=user)
    permuts = []
    for permut_assoc in permuts_assoc:
        # get the permut information
        permut = Permut.objects.get(permut_id=permut_assoc.permut_id.permut_id)
        place = Place.objects.get(place_id=permut_assoc.place_id.place_id)
        contact = MaieuclicUser.objects.get(email=permut_assoc.email)
        if contact.phone_authorization:
            try:
                phone = contact.phone
            except AttributeError:
                phone = "La personne qui libère ce poste n'a pas renseigné son numéro de téléphone."
        else:
            phone = "La personne qui libère ce poste ne nous a pas autorisés à vous communiquer son numéro de téléphone."
        if contact.email_authorization:
            email = contact.email
        else:
            email = "La personne qui libère ce poste ne nous a pas autorisés à vous communiquer son adresse mail."
        permutation = {
            'place': "{} ({})".format(place.city, place.zipcode),
            'mail': email,
            'phone': phone
        }
        permuts.append(permutation)
        # Change permut_state if wished.
        if request.method == "POST":
            form = PermutStateForm(request.POST)
            if form.is_valid():
                # pb ici : est-ce que j'affiche par def l'etat de la permut ?
                data = form.cleaned_data
                permut.permut_state = data['permut_state']
                permut.save()
                # setting the user_state for each user involved in the permutation
                emails = permut.users
                for people in emails:
                    user_involved = MaieuclicUser.objects.get(email=people)
                    if data['permut_state'] == 'CR' or 'RE' or 'NO':
                        user_involved.user_state = True
                    else:
                        user_involved.user_state = False
                    user_involved.save()
                return render(request, 'my_permut.html', locals())
            else:
                error = True
        else:
            form = PermutStateForm()
            form.fields['permut_state'].initial = permut.permut_state

    return render(request, 'my_permut.html', locals())
