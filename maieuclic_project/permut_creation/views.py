from django.shortcuts import render
from .forms import PlaceForm
from .models import Place, PermutSearch
from user.models import MaieuclicUser

# Create your views here.


def permut_creation(request):
    print(request)
    error = False
    if request.method == "POST" and 'save_permut_search' in request.POST:
        search_form = PlaceForm(request.POST)
        if search_form.is_valid():
            city = search_form.cleaned_data['city']
            zipcode = search_form.cleaned_data['zipcode']
            places = Place.objects.filter(city__exact=city, zipcode__exact=zipcode)
            if not places:
                Place.objects.create_place(city, zipcode, "")
                places = Place.objects.filter(city__exact=city, zipcode__exact=zipcode)
            for place in places:
                place_searched = PermutSearch.objects.save_searched_place(place.place_id, request.user.email)
            return render(request, 'permut_search.html', locals())
        else:
            error = True

    elif request.method == "POST" and 'save_permut_leave' in request.POST:
        leave_form = PlaceForm(request.POST)
        if leave_form.is_valid():
            city = leave_form.cleaned_data['city']
            zipcode = leave_form.cleaned_data['zipcode']
            place_left = Place.objects.create_place(city, zipcode)
            MaieuclicUser.save_place_left(request.user.email, place_left.place_id)
        else:
            error = True
    else:
        search_form = PlaceForm()
        leave_form = PlaceForm()
    return render(request, 'permut_search.html', locals())
