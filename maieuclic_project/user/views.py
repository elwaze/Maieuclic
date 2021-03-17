from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import MaieuclicUser
from .forms import SigninForm, SignupForm, AccountForm
from .tokens import account_activation_token

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
                # return my_account(request)
            else:
                # prompts an error
                error = True
    else:
        form = SigninForm()

    return render(request, 'signin.html', locals())


# signout
@login_required
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
            # creating user
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
            alt_text_content = ("Bonjour, veuillez copier le lien suivant pour activer votre compte Maïeuclic "
                                "et le coller dans votre navigateur: {}user/activate/{}/{}/").format(
                context['domain'], context['uid'], context['token'])

            email = EmailMultiAlternatives(
                subject, alt_text_content, 'maieuclic@gmail.com', to_email
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
@login_required
def my_account(request):
    """
    Getting the user's personal page.
    """
    error = False
    user = request.user

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            # checking form data
            data = form.cleaned_data
            user.phone_number = data['phone_number']
            user.first_name = data['first_name']
            user.phone_authorization = data['phone_authorization']
            user.email_authorization = data['email_authorization']
            user.save()
            return render(request, 'my_account.html', locals())

        else:
            error = True
    else:
        # initiating form with data from DB
        form = AccountForm()
        form.fields['phone_number'].initial = user.phone_number
        form.fields['first_name'].initial = user.first_name
        form.fields['phone_authorization'].initial = user.phone_authorization
        form.fields['email_authorization'].initial = user.email_authorization

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


# def delete_account(request):
#     pass
