from django.urls import path
from . import views



urlpatterns = [
    path('view-notifications/', views.view_notification, name='view_notifications')
]