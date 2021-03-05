import ast
import json
import locale
import re
import urllib
from urllib.request import urlopen

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Model, Q
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django_quill.quill import Quill

from core.models import Questions, Cities, User, MatchPrisoner, Prisoner, Message, MatchPages, GroupPage, ForumCategory, \
    ForumPost, ForumComment, MatchForumComment

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import RequestInfoForm, RequestInfoFormOnline, SignUpForm, MessagesForm, ForumPostForm


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


def get_prisoners(user_id):
    prisoners = ()
    for user in MatchPrisoner.objects.all():
        if user.user_id.id == user_id:
            prisoners = prisoners + ((user.user_id, user.prisoner_id),)
    return prisoners


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


@login_required(login_url='login')
def message_view(request):
    messages = Message.objects.filter(Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)) \
        .order_by('receiver_id', 'sender_id', '-date').distinct('receiver_id', 'sender_id')
    messages = Message.objects.filter(id__in=messages).order_by('-date')
    new_objcts = set()
    new_msgs = []
    for m in messages:
        if m.receiver.id < m.sender.id:
            temp = tuple([m.receiver.id, m.sender.id])
            if temp not in new_objcts:
                new_objcts.add(temp)
                new_msgs.append(m)
        else:
            temp = tuple([m.sender.id, m.receiver.id])
            if temp not in new_objcts:
                new_objcts.add(temp)
                new_msgs.append(m)

    print(new_msgs)
    return render(request, 'profile/message.html', {'messages': new_msgs})


@login_required(login_url='login')
def client_message(request, id):
    messages = Message.objects.filter(Q(Q(sender_id=id) & Q(receiver_id=request.user.id)) |
                                      Q(Q(sender_id=request.user.id) & Q(receiver_id=id))) \
        .order_by('receiver_id', 'sender_id')
    messages = Message.objects.filter(id__in=messages).order_by('-date')[:5]
    for m in messages:
        if not m.viewed and m.sender.id is not request.user.id:
            m.viewed = True
            m.save()
    contact_to = User.objects.get(id=id)
    form = MessagesForm()
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        text = form.data['text']
        if form.is_valid():
            message = Message.objects.create(receiver_id=id, sender_id=request.user.id, text=text)
            message.save()
            return redirect('messages', id)
    return render(request, 'profile/conversation.html', {'messages': messages, 'contact': contact_to, 'form': form})


@login_required(login_url='login')
def load_more(request):
    id = int(request.POST['id'])
    offset = int(request.POST['offset'])
    limit = 5
    messages = Message.objects.filter(Q(Q(sender_id=id) & Q(receiver_id=request.user.id)) |
                                      Q(Q(sender_id=request.user.id) & Q(receiver_id=id))) \
        .order_by('receiver_id', 'sender_id')
    totaldata = messages.count()

    messages = Message.objects.filter(id__in=messages).order_by('-date')[offset:limit + offset]
    new_list = []
    for m in messages:
        print(m.id, offset, m.date)
        if m.sender.id == request.user.id:
            d = {'username': m.sender.first_name + " " + m.sender.last_name,
                 'date': m.date.strftime("%d. %B %Y %H:%M"),
                 'received': False,
                 'text': str(m.text)}
        else:
            d = {'username': m.sender.first_name + " " + m.sender.last_name,
                 'date': m.date.strftime("%d. %B %Y %H:%M"),
                 'received': True,
                 'text': str(m.text)}
        new_list.append(d)
    posts_json = json.dumps(new_list)
    # posts_json = serializers.serialize('json', messages, fields=('text'))
    return JsonResponse(data={
        'posts': posts_json,
        'totalResults': totaldata
    })


@login_required(login_url='login')
def load_users(request):
    if request.is_ajax():
        term = request.GET.get('term')
        users = User.objects.filter(Q(username__contains=term) | Q(first_name__contains=term) |
                                    Q(last_name__contains=term))
        response_content = list(users.values())
        return JsonResponse(response_content, safe=False)


@login_required(login_url='login')
def new_message(request):
    users = User.objects.all()
    form = MessagesForm()
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        user = request.POST['user_select']
        if form.is_valid() and user is not None:
            print("re")
            message = Message.objects.create(receiver_id=user, sender_id=request.user.id, text=request.POST['text'])
            message.save()
            return redirect('messages_page')
    return render(request, 'profile/new_message.html', {'users': users, 'form': form})


def load_departments():
    with urllib.request.urlopen(
            "https://services-eu1.arcgis.com/v8rjTx8d1cMu13Tc/ArcGIS/rest/services/ustavy/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&f=pjson&outSr=4326") as url:
        data = json.loads(url.read().decode())
    department = []
    for d in data['features']:
        id = d['attributes']['FID']
        name = d['attributes']['Miesto']
        type = d['attributes']['Typ_ústav']
        info = d['attributes']['ÚSTAV']
        address = d['attributes']['Adresa']
        match = re.search(r'href=[\'"]mailto:?([^\'" >]+)', d['attributes']['E_mail'])
        email = None
        if match:
            email = match.group(1)

        tel = d['attributes']['Tel_']

        match = re.search(r'href=[\'"]?([^\'" >]+)', d['attributes']['Web'])
        web = None
        if match:
            web = match.group(1)

        department.append({'FID': id, 'name': name, 'type': type, 'info': info, 'address': address, 'email': email,
                           'tel': tel, 'web': web})
    return department


def departments(request):
    department = load_departments
    return render(request, 'departments.html', {'data': department})


@login_required(login_url='login')
def profile_view(request):
    prisoners = get_prisoners(request.user.id)
    department = load_departments()
    new_dict = {}
    list_of_prisoners = []
    for prisoner in prisoners:
        new_dict = {"prisoner": prisoner, "departments":
            next(item for item in department if item["FID"] == prisoner[1].id)}
        list_of_prisoners.append(new_dict)

    return render(request, 'profile.html', {'list_of_prisoners': list_of_prisoners})


def support(request):
    groups = GroupPage.objects.all()
    nl = []
    for group in groups:
        page = MatchPages.objects.all().filter(group=group)
        nl.append({"group": group, "page": page})
    return render(request, 'podpora.html', {'matches': nl})


@login_required(login_url='login')
def forum_view(request):
    categories = ForumCategory.objects.all()
    result = []
    for category in categories:
        posts = ForumPost.objects.filter(category_id=category.id)
        list_post = []
        for post in posts:
            c = MatchForumComment.objects.filter(forum_post_id=post.id).order_by('-forum_comment__edited_at').first()
            list_post.append({'post': post, 'comment': c})
        new_d = {'category': category, 'posts': list_post}
        result.append(new_d)
    print(result)
    return render(request, 'forum/forum.html', {'result': result})


@login_required(login_url='login')
def category_view(request, category_id):
    category = ForumCategory.objects.get(id=category_id)
    posts = ForumPost.objects.filter(category_id=category_id)
    list_post = []
    for post in posts:
        c = MatchForumComment.objects.filter(forum_post_id=post.id).order_by('-forum_comment__edited_at').first()
        list_post.append({'post': post, 'comment': c})
    return render(request, 'forum/category.html', {'category': category, 'result': list_post})


@login_required(login_url='login')
def post_view(request, post_id):
    post = ForumPost.objects.filter(id=post_id).first()
    match = MatchForumComment.objects.filter(forum_post=post_id)
    paginator = Paginator(match, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ForumPostForm()
    return render(request, 'forum/post.html', {'post': post, 'comments': page_obj, 'form': form})


def get_quill(delta, html):
    quill = Quill({
        'delta': delta,
        'html': html,
    })
    return quill


@login_required()
def send_forum_post(request):
    if request.method == 'POST':
        # form = ForumPostForm(request.POST)
        # if form.is_valid():
        html = request.POST['html'].rsplit('"', 1)[0]
        html = html.rsplit('"', 1)[1]
        quill = get_quill(request.POST['text'], html)
        post = ForumPost.objects.filter(id=request.POST['post_id']).first()
        comment = ForumComment.objects.create(text=quill, creator_id=request.user.id)
        match = MatchForumComment.objects.create(forum_comment=comment, forum_post=post)
        return HttpResponse("Success")
    return HttpResponse("Fail")
