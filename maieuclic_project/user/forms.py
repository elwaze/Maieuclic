from django import forms


class ConnectionForm(forms.Form):
    # Form for connection.
    pass


class AccountForm(ConnectionForm):
    # Form to create a new account.
    pass
