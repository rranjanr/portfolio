from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Story routes disabled for now
    # path('stories/', views.stories, name='stories'),
    # path('stories/new/', views.story_new, name='story_new'),
    # path('stories/<slug:slug>/edit/', views.story_edit, name='story_edit'),
    # path('stories/<slug:slug>/', views.story_detail, name='story_detail'),
    path('gallery/new/', views.gallery_new, name='gallery_new'),
    path('send-message/', views.send_message, name='send_message'),
    path('test-email/', views.test_email, name='test_email'),
] 