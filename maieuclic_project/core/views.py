from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
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
        message = form.cleaned_data['message']
        context = {
            'message': message
        }
        sender = form.cleaned_data['sender']
        send_copy = form.cleaned_data['send_copy']
        to_email = ["maieuclic@gmail.com"]
        if send_copy:
            to_email.append(sender)
        email_content = render_to_string('contact_email.html', context)
        alt_text_content = "Bonjour, Le message suivant a été envoyé à Maïeuclic : {}".format(message)
        email = EmailMultiAlternatives(
            subject, alt_text_content, sender, to_email
        )
        email.attach_alternative(email_content, "text/html")
        response = email.send()
        sending = True
    return render(request, 'contact.html', locals())

# from django.core.mail import EmailMultiAlternatives
#
# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()
