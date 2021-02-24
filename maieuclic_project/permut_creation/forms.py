from django import forms


class PlaceForm(forms.Form):
    # form to define the place the user is looking for or leaving
    city = forms.CharField(label="Ville")
    zipcode = forms.CharField(label="Code postal", max_length=5, min_length=5)
