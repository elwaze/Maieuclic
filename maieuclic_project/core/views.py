from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from.forms import ContactForm

# Create your views here.


# home
def home(request):
    return render(request, 'home.html')


# legal notices
def legal_notices(request):
    return render(request, 'legal_notices.html')


# contact with e-mail form
def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        context = {
            'message': form.cleaned_data['message']
        }
        # message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        send_copy = form.cleaned_data['send_copy']
        to_email = ["maieuclic@gmail.com"]
        if send_copy:
            to_email.append(sender)
        email_content = render_to_string('contact_email.html', context)
        email = EmailMessage(
            subject, email_content, to=to_email, from_email=sender
        )
        response = email.send()
        sending = True
    return render(request, 'contact.html', locals())
