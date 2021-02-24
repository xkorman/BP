import datetime

from django import forms
from functools import partial

from django.contrib.auth.forms import UserCreationForm
from django.forms import Select

from Test_BP import settings
from core.models import User, Cities

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class RequestInfoForm(forms.Form):
    client_name = forms.CharField(label='Povinná osoba, ktorej je žiadosť určená: ', required=False)
    client_address = forms.CharField(label='Adresa povinnej osoby:', required=False)
    sender_name = forms.CharField(label='Meno a priezvisko, názov alebo obchodné meno žiadateľa:', required=False)
    sender_address = forms.CharField(label='Adresa pobytu alebo sídlo žiadateľa: ', required=False)
    sender_address.help_text = 'ulica, číslo domu, mesto, PSČ'
    way = forms.CharField(label='Požadovaný spôsob sprístupnenia informácií:', required=False)
    info = forms.CharField(label='Požadované informácie:', required=False)
    date = forms.DateField(widget=DateInput(), label='Dátum', required=False)


class RequestInfoFormOnline(forms.Form):
    client_name = forms.CharField(label='Povinná osoba, ktorej je žiadosť určená: ', required=True)
    client_address = forms.CharField(label='Adresa povinnej osoby:', required=True)
    sender_name = forms.CharField(label='Meno a priezvisko, názov alebo obchodné meno žiadateľa:', required=True)
    sender_address = forms.CharField(label='Adresa pobytu alebo sídlo žiadateľa: ', required=True)
    sender_address.help_text = 'ulica, číslo domu, mesto, PSČ'


class SignUpForm(UserCreationForm):
    city = forms.ModelChoiceField(label='Obec', queryset=Cities.objects.all())
    street = forms.CharField(label='Ulica', required=True)
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'], widget=DateInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'sex', 'city', 'street',
                  'date_of_birth')
