from django import forms


class PlaceSearchedForm(forms.Form):
    # form to define the place the user is looking for
    city = forms.CharField(label="Ville")
    zipcode = forms.CharField(label="Code postal", max_length=5, min_length=5)


class PlaceLeftForm(PlaceSearchedForm):
    # form to define the place the user wants to leave

    hospital_name = forms.CharField(label="hôpital")

