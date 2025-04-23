from django.urls import include, path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main Pages
    path('', views.landing_page, name='landing_page'),
    path('videos/', views.videos_page, name='videos'),
    path('sponsorships/', views.sponsor_page, name='sponsorships'),
    path('profile/', views.profiles, name='profile'),
    path('profiles/', views.profiles, name='profiles'),
    path('home/', views.home, name='home'),
    path('candidates_page/', views.candidates_page, name='candidates_page'),
    path('candidates_register/', views.candidates_register, name='candidates_register'),
    path('top_contributors/', views.top_contributors, name='top_contributors'),
    path('progress_tracking/', views.progress_tracking, name='progress_tracking'),
    path('mentoring_schedule/', views.mentoring_schedule, name='mentoring_schedule'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create_officer/', views.create_officer, name='create_officer'),
    path('create_member/', views.create_member, name='create_member'),
    path('create_guest/', views.create_guest, name='create_guest'),
    path('logout/', views.logout_view, name='logout'),

    # Session Management
    path('create_startup/', views.create_session, name='create_session'),
    path('startup/<int:session_id>/', views.session_view, name='session_view'),
    path('join/<int:invite_code>/', views.process_invite, name='process_invite'),
    path('join_startup/<int:session_id>/', views.join_session, name='join_session'),
    path('my_startups/', views.session_list, name='session_list'),

    # Forum and Helpdesk
    path('public-forum/', views.public_forum, name='public_forum'),
    path("helpdesk/", views.helpdesk, name="helpdesk"),
    path('helpdesk/send/', views.helpdesk_send, name='helpdesk_send'),
    path('helpdesk/messages/', views.helpdesk_messages, name='helpdesk_messages'),

    # Profiles
    path('profiles/', views.profiles, name='profiles'),
    path('my_profile/', views.profile, name='profile'),
    path('officer_profiles/', views.officer_profiles, name='officer_profiles'),
    path('member_profiles/', views.member_profiles, name='member_profiles'),

    # Content Management
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),
    path('mark_as_favorite/<int:post_id>/', views.mark_as_favorite, name='mark_as_favorite'),
    path('favorite-posts/', views.favorite_posts, name='favorite_posts'),
    path('announcement/<int:announcement_id>/', views.view_announcement, name='view_announcement'),

    # Resources and Inbox
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:resource_id>/experts/', views.experts_by_resource, name='experts_by_resource'),
    path('experts/<int:expert_id>/', views.expert_detail, name='expert_detail'),
    path('connect/<int:expert_id>/', views.connect_to_expert, name='connect_to_expert'),
    path('inbox/', views.inbox, name='inbox'),
    path('send/', views.send_correspondence, name='send_correspondence'),
    path('mark-as-read/<int:msg_id>/', views.mark_as_read, name='mark_as_read'),

    # Static/Media Files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)