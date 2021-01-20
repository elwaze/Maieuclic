from django import forms
from .models import MaieuclicUser
from django.core.exceptions import ValidationError


class SigninForm(forms.Form):
    # Form for connection.
    email = forms.EmailField(label="Identifiant : e-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SignupForm(SigninForm):
    # Form to create a new account.
    pwd_confirm = forms.CharField(label="Confirmation mot de passe", widget=forms.PasswordInput)

    def clean_email(self):
        # Checking username validity.
        if MaieuclicUser.objects.filter(email=self.data['email']).exists():
            raise ValidationError("Ce nom d'utilisateur existe déjà.")
        return self.data['email']

    def clean_pwd_confirm(self):
        # Checking that the confirmation password is the same than the first password.
        if self.data['password'] != self.data['pwd_confirm']:
            raise ValidationError("veuillez entrer un mot de passe de confirmation identique au mot de passe choisi. ")
