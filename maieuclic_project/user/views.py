from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .models import MaieuclicUser
from .forms import SigninForm, SignupForm, AccountForm
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives

# Create your views here.


# signin
def signin(request):
    """
     Connection to the user account.
    """

    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Checking identification data
            user = authenticate(email=email, password=password)
            if user:
                # Connecting user
                login(request, user)
                return render(request, 'my_account.html', locals())
            else:
                # prompts an error
                error = True
    else:
        form = SigninForm()

    return render(request, 'signin.html', locals())


# signout
def signout(request):
    """
    Logging the user out.
    """

    logout(request)
    return render(request, 'home.html', locals())


# create_account
def signup(request):
    """
    Creating a new user account.
    """

    error = False

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # checking form data
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Creating user
            user = MaieuclicUser.objects.create_user(email, password)
            user.is_active = False
            user.save()
            # sending confirmation email
            subject = 'Finalisez la création de votre compte Maieuclic'
            context = {
                'user': user,
                'domain': settings.SITE_LINK,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
                }
            email_content = render_to_string('confirmation_email.html', context)
            to_email = [form.cleaned_data.get("email")]
            alt_text_content = "Bonjour, veuillez cliquer sur le lien suivant pour activer votre compte Maïeuclic : "

            email = EmailMultiAlternatives(
                subject, alt_text_content, 'do_not_reply@maieuclic.com', to_email
            )
            email.attach_alternative(email_content, "text/html")
            response = email.send()
            sending = True
            activation = 'Veuillez confirmer votre adresse email pour valider la création de votre compte Maieuclic'

            return render(request, 'signup.html', locals())

        else:
            error = True
    else:
        form = SignupForm()
    return render(request, 'signup.html', locals())


# my_account
def my_account(request):
    """
    Getting the user's personal page.
    """
    error = False
    user = request.user

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.phone = data['phone']
            user.set_password(data['password'])
            user.phone_authorization = data['phone_authorization']
            user.mail_authorization = data['mail_authorization']
            user.save()
            return render(request, 'my_account.html', locals())

        else:
            error = True
    else:
        form = AccountForm()
    return render(request, 'my_account.html', locals())


def activate(request, uidb64, token):
    """
    sets the user.is_active to true if the token is valid,
    login the user, redirects to the my_account page.
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MaieuclicUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MaieuclicUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('my_account')
    else:
        return HttpResponse('Le lien d\'activation est invalide, veuillez réessayer !')


def change_my_account(request, field, value):
    pass


def delete_account(request):
    pass
