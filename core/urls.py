from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import InfoView, get_request_data, get_info_request, profile_view, related_view, requests_view, signup
urlpatterns = [
    # path('index', views.index),
    path('', InfoView.as_view(), name='InfoView'),
    path('', include('django.contrib.auth.urls')),
    path('faq', views.faq, name='faq'),
    path('ziadost/info', get_request_data, name='ziadost_info'),
    path('ziadost/info_logged_in', get_info_request, name='ziadost_info_logged_in'),
    path('profil', profile_view, name='profile'),
    path('profil/pribuzny', related_view, name='related'),
    path('profil/ziadosti', requests_view, name='requests'),
    path('register', signup, name='register'),
]