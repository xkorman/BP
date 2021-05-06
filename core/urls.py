from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import InfoView, get_request_data, get_info_request, profile_view, related_view, requests_view, signup, \
    message_view, client_message, new_message

urlpatterns = [
    # path('index', views.index),
    path('', views.InfoView, name='InfoView'),
    path('', include('django.contrib.auth.urls')),
    path('faq', views.faq, name='faq'),
    path('ziadost/info', get_request_data, name='ziadost_info'),
    # path('get_prisoner_values', views.get_prisoner_values, name='get_prisoner_values'),
    path('ziadost/info_logged_in', get_info_request, name='ziadost_info_logged_in'),
    path('ziadost/bankove_spojenie', views.money, name='money'),
    path('ziadost/navsteva', views.visit, name='visit'),
    path('ziadost/detail=<int:req_id>', views.info_detail, name='info_detail'),
    path('profil', profile_view, name='profile'),
    path('profil/pribuzny', related_view, name='related'),
    path('profil/ziadosti', requests_view, name='requests'),
    path('register', signup, name='register'),
    path('profil/spravy', message_view, name='messages_page'),
    path('profil/spravy/<int:id>/', client_message, name='messages'),
    path('profil/spravy/nova_sprava/', new_message, name='new_message'),
    path('load-more', views.load_more, name='load_more'),
    path('load-users', views.load_users, name='load_users'),
    path('ustavy/', views.departments, name='departments'),
    path('podpora/', views.support, name='support'),
    path('forum/', views.forum_view, name='forum_view'),
    path('forum/kategoria/<int:category_id>', views.category_view, name='category_view'),
    path('forum/prispevok/<int:post_id>', views.post_view, name='post_view'),
    path('forum/send_comment', views.send_forum_post, name='send_forum_post'),
    path('forum/delete_comment', views.delete_comment, name='delete_comment'),
    path('forum/editovat_prispevok/<int:post_id>', views.edit_post, name='edit_post'),
    path('forum/editovat_komentar/<int:post_id>', views.edit_comment, name='edit_comment'),
    path('forum/edit_comment_back', views.edit_comment_back, name='edit_comment_back'),
    path('forum/edit_comment_back2', views.edit_comment_back2, name='edit_comment_back2'),
    path('forum/novy_prispevok/', views.new_post, name='new_post')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
