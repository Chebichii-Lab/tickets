# Ticketer/persons/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from persons.models import Person

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.CharField(max_length=150, help_text='Required')

    class Meta:
        model = Person
        fields = ('email', 'username', 'password1', 'password2')


class TopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
