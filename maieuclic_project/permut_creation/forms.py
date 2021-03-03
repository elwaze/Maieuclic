from django import forms


class PlaceForm(forms.Form):
    """Form to define the place the user is looking for or leaving."""
    city = forms.CharField(label="Ville")
    zipcode = forms.CharField(label="Code postal", max_length=5, min_length=5)
