import datetime

from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class RequestInfoForm(forms.Form):
    client_name = forms.CharField(label='Povinná osoba, ktorej je žiadosť určená: ')
    client_address = forms.CharField(label='Adresa povinnej osoby:')
    sender_name = forms.CharField(label='Meno a priezvisko, názov alebo obchodné meno žiadateľa:')
    sender_address = forms.CharField(label='Adresa pobytu alebo sídlo žiadateľa: ')
    sender_address.help_text = 'ulica, číslo domu, mesto, PSČ'
    way = forms.CharField(label='Požadovaný spôsob sprístupnenia informácií:')
    info = forms.CharField(label='Požadované informácie:')
    date = forms.DateField(widget=DateInput(), label='Dátum', required=False,)
