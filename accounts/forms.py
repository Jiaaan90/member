# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField


class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email','name','phone','birth_date')
        widget = {
            'birth_date' : DateInput(),
        }
class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': 'True'}))

