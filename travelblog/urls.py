from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('add-post/', views.add_post, name='add_post'),

    path('process-add-post/', views.process_add_post, name='process_add_post'),
]