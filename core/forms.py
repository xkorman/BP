import datetime

from django import forms
from functools import partial

from django.contrib.auth.forms import UserCreationForm
from django.forms import Select, ModelForm
from django_quill.forms import QuillFormField

from Test_BP import settings
from core.models import User, Cities, ForumCategory, Requests

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
    text = forms.CharField(widget=forms.Textarea, required=True, label='Text žiadosti')


class SignUpForm(UserCreationForm):
    city = forms.ModelChoiceField(label='Obec', queryset=Cities.objects.all())
    street = forms.CharField(label='Ulica', required=True)
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'], widget=DateInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'sex', 'city', 'street',
                  'date_of_birth')


class MessagesForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)


class ForumPostForm(forms.Form):
    text = QuillFormField()

    class Media:
        js = ('js/forum_post.js',)


class ForumEditForm(forms.Form):
    title = forms.CharField()
    text = QuillFormField()

    class Media:
        js = ('js/edit_post.js',)


class ForumCreateForm(forms.Form):
    category = forms.ModelChoiceField(queryset=ForumCategory.objects.all(), empty_label=None, required=True)
    title = forms.CharField(required=True)
    text = QuillFormField()

    class Media:
        js = ('js/create_post.js',)


class RequestVisitForm(ModelForm):
    class Meta:
        model = Requests
        fields = ['prisoner', 'type', 'reason']
        labels = {'prisoner': 'Väzeň',
                  'type': 'Typ žiadosti',
                  'reason': 'Odôvodnenie'}

