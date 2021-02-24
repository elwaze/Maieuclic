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
        return self.data['pwd_confirm']


class AccountForm(forms.Form):
    # form to fill or change account fields
    # password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    # pwd_confirm = forms.CharField(label="Confirmation mot de passe", widget=forms.PasswordInput)
    first_name = forms.CharField(label="prénom", max_length=30)
    phone_number = forms.CharField(label="téléphone", max_length=10)
    phone_authorization = forms.BooleanField(label="j'autorise la communication de mon numéro de téléphone aux personnes identifiées dont les souhaits correspondent à une permutation avec moi", required=False)
    email_authorization = forms.BooleanField(label="j'autorise la communication de mon adresse e-mail aux personnes identifiées dont les souhaits correspondent à une permutation avec moi", required=False)

    # def clean_pwd_confirm(self):
    #     # Checking that the confirmation password is the same than the first password.
    #     if self.data['password'] != self.data['pwd_confirm']:
    #         raise ValidationError("veuillez entrer un mot de passe de confirmation identique au mot de passe choisi. ")
