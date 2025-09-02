from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add-trip/', views.add_trip, name='add_trip'),
    path('proces-add-trip', views.process_add_trip, name='process_add_trip'),
    path('download/<int:id>/', views.download, name='download'),
    path('statistics/', views.statistics, name='statistics'),
    path('request-process-add-trip/', views.request_process_add_trip, name='request_process_add_trip'),

]