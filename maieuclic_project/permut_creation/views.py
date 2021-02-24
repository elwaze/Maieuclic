from django.shortcuts import render
from .forms import PlaceForm
from .models import Place, PermutSearch
from user.models import MaieuclicUser

# Create your views here.


def permut_creation(request):
    print(request)
    error = False
    if request.method == "POST":
        search_form = PlaceForm(request.POST, prefix="search")
        if search_form.is_valid():
            city = search_form.cleaned_data['city']
            zipcode = search_form.cleaned_data['zipcode']
            place = Place.objects.create_place(city, zipcode)[0]
            print('place searched')
            print(place)
            print(place.place_id, place.city, place.zipcode)
            place_searched = PermutSearch.objects.save_searched_place(place, request.user)

            return render(request, 'permut_search.html', locals())
        else:
            error = True

        leave_form = PlaceForm(request.POST, prefix="leave")
        if leave_form.is_valid():
            city = leave_form.cleaned_data['city']
            print(city)
            zipcode = leave_form.cleaned_data['zipcode']
            print(zipcode)
            place_left = Place.objects.create_place(city, zipcode)[0]
            print("place left")
            print(place_left)
            print(place_left.city)
            print(place_left.zipcode)
            print(place_left.place_id)
            MaieuclicUser.objects.save_place_left(request.user.email, place_left)
            return render(request, 'permut_search.html', locals())

        else:
            error = True

    else:
        search_form = PlaceForm(prefix="search")
        try:
            # boucle for pour tous les places + 1
            # ajouter id dans le form avec id de la recherche en DB
            # cf formset
            place_searched = PermutSearch.objects.filter(email=request.user)[0].place_id
            print('place_searched')
            print(place_searched)
            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
        except IndexError:
            pass
        # place_searched = Place.objects.get(pk=place_searched.place_id)

        leave_form = PlaceForm(prefix="leave")
        try:
            place_left = Place.objects.get(pk=request.user.place_id.place_id)
            print('place_left')
            print(place_left.city)
            leave_form.fields['city'].initial = place_left.city
            leave_form.fields['zipcode'].initial = place_left.zipcode
        except AttributeError:
            pass
    return render(request, 'permut_search.html', locals())


def leave_place(request):
    error = False
    if request.method == "POST":

        leave_form = PlaceForm(request.POST, prefix="leave")
        if leave_form.is_valid():
            city = leave_form.cleaned_data['city']
            print(city)
            zipcode = leave_form.cleaned_data['zipcode']
            print(zipcode)
            place_left = Place.objects.create_place(city, zipcode)[0]
            print("place left")
            print(place_left)
            print(place_left.city)
            print(place_left.zipcode)
            print(place_left.place_id)
            MaieuclicUser.objects.save_place_left(request.user.email, place_left)
            search_form = PlaceForm(prefix="search")
            try:
                # boucle for pour tous les places + 1
                # ajouter id dans le form avec id de la recherche en DB
                # cf formset
                place_searched = PermutSearch.objects.filter(email=request.user)[0].place_id
                print('place_searched')
                print(place_searched)
                search_form.fields['city'].initial = place_searched.city
                search_form.fields['zipcode'].initial = place_searched.zipcode
            except IndexError:
                pass

            return render(request, 'permut_search.html', locals())

        else:
            error = True

    else:
        search_form = PlaceForm(prefix="search")
        try:
            # boucle for pour tous les places + 1
            # ajouter id dans le form avec id de la recherche en DB
            # cf formset
            place_searched = PermutSearch.objects.filter(email=request.user)[0].place_id
            print('place_searched')
            print(place_searched)
            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
        except IndexError:
            pass
        # place_searched = Place.objects.get(pk=place_searched.place_id)

        leave_form = PlaceForm(prefix="leave")
        try:
            place_left = Place.objects.get(pk=request.user.place_id.place_id)
            print('place_left')
            print(place_left.city)
            leave_form.fields['city'].initial = place_left.city
            leave_form.fields['zipcode'].initial = place_left.zipcode
        except AttributeError:
            pass
    return render(request, 'permut_search.html', locals())


def search_place(request):
    error = False
    if request.method == "POST":
        search_form = PlaceForm(request.POST, prefix="search")
        if search_form.is_valid():
            city = search_form.cleaned_data['city']
            zipcode = search_form.cleaned_data['zipcode']
            place = Place.objects.create_place(city, zipcode)[0]
            print('place searched')
            print(place)
            print(place.place_id, place.city, place.zipcode)
            place_searched = PermutSearch.objects.save_searched_place(place, request.user)
            leave_form = PlaceForm(prefix="leave")
            try:
                place_left = Place.objects.get(pk=request.user.place_id.place_id)
                print('place_left')
                print(place_left.city)
                leave_form.fields['city'].initial = place_left.city
                leave_form.fields['zipcode'].initial = place_left.zipcode
            except AttributeError:
                pass

            return render(request, 'permut_search.html', locals())
        else:
            error = True

    else:
        search_form = PlaceForm(prefix="search")
        try:
            # boucle for pour tous les places + 1
            # ajouter id dans le form avec id de la recherche en DB
            # cf formset
            place_searched = PermutSearch.objects.filter(email=request.user)[0].place_id
            print('place_searched')
            print(place_searched)
            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
        except IndexError:
            pass
        # place_searched = Place.objects.get(pk=place_searched.place_id)

        leave_form = PlaceForm(prefix="leave")
        try:
            place_left = Place.objects.get(pk=request.user.place_id.place_id)
            print('place_left')
            print(place_left.city)
            leave_form.fields['city'].initial = place_left.city
            leave_form.fields['zipcode'].initial = place_left.zipcode
        except AttributeError:
            pass
    return render(request, 'permut_search.html', locals())
