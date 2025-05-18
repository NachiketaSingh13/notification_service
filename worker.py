import pika
import json
import os
import django
import time

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from notifications.models import Notification

# Logic to simulate sending notification
def send_notification_logic(notification):
    try:
        print(f" Attempting to send {notification.type} to user {notification.user.id}...")

        # Simulate a failure for the first two retries (for testing retry logic)
        if notification.retry_count < 2:
            raise Exception("Simulated failure")  # Remove this in real-world use

        # Mark as sent
        notification.status = 'sent'
        notification.save()
        print(f" Notification {notification.id} sent successfully.")

    except Exception as e:
        print(f" Error sending notification {notification.id}: {e}")
        notification.retry_count += 1

        if notification.retry_count >= 3:
            notification.status = 'failed'
            print(f" Notification {notification.id} marked as failed after 3 attempts.")
        else:
            print(f" Retrying... Attempt {notification.retry_count}")
        
        notification.save()

# Callback for RabbitMQ
def callback(ch, method, properties, body):
    print(" Received message from queue:", body)
    data = json.loads(body)
    try:
        notification = Notification.objects.get(id=data["id"])
        send_notification_logic(notification)
    except Notification.DoesNotExist:
        print(" Notification not found in DB")

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)

print(" Worker is running... Waiting for messages.")
channel.start_consuming()
