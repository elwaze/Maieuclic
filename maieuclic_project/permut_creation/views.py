from django.shortcuts import render

from .forms import PlaceForm
from .models import Place, PermutSearch
from user.models import MaieuclicUser

# Create your views here.


def leave_place(request):
    """
    Showing/changing the place left by the user.
    """
    error = False
    if request.method == "POST":
        # save place left by the user.
        leave_form = PlaceForm(request.POST, prefix="leave")
        if leave_form.is_valid():
            city = leave_form.cleaned_data['city']
            zipcode = leave_form.cleaned_data['zipcode']
            place_left = Place.objects.create_place(city, zipcode)[0]
            MaieuclicUser.objects.save_place_left(request.user.email, place_left)

            # get place(s) left by the user.
            search_forms = []
            places_searched = PermutSearch.objects.filter(email=request.user)
            for permut in places_searched:
                place_searched = permut.place_id
                search_form = PlaceForm(prefix="search")

                search_form.fields['city'].initial = place_searched.city
                search_form.fields['zipcode'].initial = place_searched.zipcode
                search_forms.append(search_form)
            search_form = PlaceForm(prefix="search")
            search_forms.append(search_form)

            return render(request, 'permut_search.html', locals())

        else:
            error = True

    else:
        # get place(s) left by the user.
        search_forms = []
        places_searched = PermutSearch.objects.filter(email=request.user)
        for permut in places_searched:
            place_searched = permut.place_id
            search_form = PlaceForm(prefix="search")

            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
            search_forms.append(search_form)
        search_form = PlaceForm(prefix="search")
        search_forms.append(search_form)

        # get place left by the user.
        leave_form = PlaceForm(prefix="leave")
        try:
            place_left = Place.objects.get(pk=request.user.place_id.place_id)
            leave_form.fields['city'].initial = place_left.city
            leave_form.fields['zipcode'].initial = place_left.zipcode
        except AttributeError:
            pass
    return render(request, 'permut_search.html', locals())


def search_place(request):
    """
    Showing/changing the place(s) searched by the user.
    """
    error = False
    if request.method == "POST":
        # save place(s) searched by the user.
        search_forms = []
        places_searched = PermutSearch.objects.filter(email=request.user)
        for permut in places_searched:
            place_searched = permut.place_id
            search_form = PlaceForm(prefix="search")
            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
            search_forms.append(search_form)
        search_form = PlaceForm(request.POST, prefix="search")
        if search_form.is_valid():
            city = search_form.cleaned_data['city']
            zipcode = search_form.cleaned_data['zipcode']
            place = Place.objects.create_place(city, zipcode)[0]
            place_searched = PermutSearch.objects.save_searched_place(place, request.user)
            search_forms.append(search_form)
            search_form = PlaceForm(prefix="search")
            search_forms.append(search_form)

            # get place left by the user.
            leave_form = PlaceForm(prefix="leave")
            try:
                place_left = Place.objects.get(pk=request.user.place_id.place_id)
                leave_form.fields['city'].initial = place_left.city
                leave_form.fields['zipcode'].initial = place_left.zipcode
            except AttributeError:
                pass

            return render(request, 'permut_search.html', locals())
        else:
            error = True

    else:
        # get place(s) searched by the user.
        search_forms = []
        places_searched = PermutSearch.objects.filter(email=request.user)
        for permut in places_searched:
            place_searched = permut.place_id
            search_form = PlaceForm(prefix="search")

            search_form.fields['city'].initial = place_searched.city
            search_form.fields['zipcode'].initial = place_searched.zipcode
            search_forms.append(search_form)
        search_form = PlaceForm(prefix="search")
        search_forms.append(search_form)

        # get place left by the user.
        leave_form = PlaceForm(prefix="leave")
        try:
            place_left = Place.objects.get(pk=request.user.place_id.place_id)
            leave_form.fields['city'].initial = place_left.city
            leave_form.fields['zipcode'].initial = place_left.zipcode
        except AttributeError:
            pass
    return render(request, 'permut_search.html', locals())
