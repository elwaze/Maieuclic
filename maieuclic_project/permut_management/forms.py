from django import forms
from .models import Permut


class PermutStateForm(forms.Form):
    # Form to change permut state.
    permut_state = forms.ChoiceField(label="Etat de la permutation", choices=Permut.states)
