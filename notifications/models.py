from django.db import models


NOTIFICATION_TYPES = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('in_app', 'In-App'),
]


NOTIFICATION_STATUS = [
    ('pending', 'Pending'),
    ('sent', 'Sent'),
    ('failed', 'Failed'),
]

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.type} to {self.user.name} - {self.status}"
