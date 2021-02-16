from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import InfoView, get_request_data

urlpatterns = [
    # path('index', views.index),
    path('', InfoView.as_view(), name='InfoView'),
    path('', include('django.contrib.auth.urls')),
    path('faq', views.faq, name='faq'),
    path('ziadost/info', get_request_data, name='ziadost_info'),
]