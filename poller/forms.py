from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    emailInput = forms.CharField(max_length=200)
    pinInput = forms.CharField(max_length=30)