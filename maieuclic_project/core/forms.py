from django import forms


class ContactForm(forms.Form):
    """Form to send email to maieuclic admin."""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Votre adresse e-mail")
    send_copy = forms.BooleanField(
        help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.",
        required=False
    )
