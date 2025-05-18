from django.urls import path
from . import views

urlpatterns = [
    path('notifications', views.send_notification, name='send_notification'),
    path('users/<int:user_id>/notifications', views.get_user_notifications, name='get_user_notifications'),
]
