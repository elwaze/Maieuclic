from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .forms import ContactForm
from user.models import MaieuclicUser


# Create your views here.


# home
def home(request):
    open_jobs = MaieuclicUser.objects.filter(user_state__exact=True).count()
    return render(request, 'home.html', locals())


# legal notices
def legal_notices(request):
    return render(request, 'legal_notices.html')


# contact with e-mail form
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        sender = form.cleaned_data['sender']
        to_email = ["maieuclic@gmail.com"]
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        send_copy = form.cleaned_data['send_copy']
        # add the sender e-mail in recipients if send_copy has been clicked
        if send_copy:
            to_email.append(sender)
        else:
            message = "message from : {} : {}".format(sender, message)
        context = {
            'message': message
        }
        from_email = "maieuclic@gmail.com"
        email_content = render_to_string('contact_email.html', context)
        alt_text_content = "Bonjour, Le message suivant a été envoyé à Maïeuclic : {}".format(message)
        email = EmailMultiAlternatives(
            subject, alt_text_content, from_email, to_email
        )
        email.attach_alternative(email_content, "text/html")
        response = email.send()
        sending = True
    return render(request, 'contact.html', locals())
