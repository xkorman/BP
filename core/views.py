import ast
import json
import urllib
from urllib.request import urlopen

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from core.models import Questions, Cities, User

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import RequestInfoForm, RequestInfoFormOnline, SignUpForm


class InfoView(TemplateView):
    template_name = 'home.html'


def index(request):
    return HttpResponse(template='index.html')


def faq(request):
    questions = Questions.objects.all().order_by('id')
    return render(request, 'faq.html', {'questions': questions})


def render_pdf_view(data):
    html_string = render_to_string('ziadost_info.html', {'data': data})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="mypdf.pdf"'
        return response


def get_request_data(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RequestInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.data
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render_pdf_view(data)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestInfoForm()

    return render(request, 'ziadost_info_get_data.html', {'form': form})


@login_required(login_url='login')
def get_info_request(request):
    if request.method == 'POST':
        form = RequestInfoFormOnline(request.POST)
        if form.is_valid():
            return render(request, 'online_ziadost.html')
    else:
        form = RequestInfoFormOnline
        return render(request, 'online_ziadost.html', {'form': form})
    return render(request, 'online_ziadost.html', {'form': form})


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def related_view(request):
    return render(request, 'related.html')


@login_required(login_url='login')
def requests_view(request):
    return render(request, 'requests.html')


def get_city():
    cities = Cities.objects.all().order_by('-municipalityName')
    list = []
    for city in cities:
        list2 = (city.id, city.municipalityName,)
        list.insert(0, list2)
    return list


def signup(request):
    if not request.user.is_authenticated:
        cities = get_city()
        form = SignUpForm()
        form.fields['city'].choices = cities
        if request.method == 'POST':
            form = SignUpForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                firstname = form.cleaned_data['first_name']
                lastname = form.cleaned_data['last_name']
                raw_password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                city = request.POST.get('city')
                sex = form.cleaned_data['sex']
                date_of_birth = form.cleaned_data['date_of_birth']
                user = User.objects.create(username=username, first_name=firstname, last_name=lastname, email=email,
                                           city_id=city, sex=sex, date_of_birth=date_of_birth)
                user.set_password(raw_password)
                user.save()
                return render(request, 'registration/signup1.html')
            return render(request, 'registration/signup.html', {'form': form})
        return render(request, 'registration/signup.html', {'form': form})
    else:
        logout(request)
        return HttpResponseRedirect('login')

