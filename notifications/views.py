import pika
import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Notification
from .serializers import UserSerializer, NotificationSerializer

def push_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')


    channel.basic_publish(
        exchange='',
        routing_key='notifications',
        body=json.dumps(data)
    )
    connection.close()

@api_view(['POST'])
def send_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        notification = serializer.save(status='pending')
        push_to_queue({
            "id": notification.id,
            "user_id": notification.user.id,
            "type": notification.type,
            "content": notification.content
        })

        return Response({"message": "Notification created and pending"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_notifications(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    notifications = user.notifications.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

