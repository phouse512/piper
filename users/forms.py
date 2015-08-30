from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=10, required=True)
    password = forms.CharField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)
