from django.conf import settings
from django.db import models


class Notification(models.Model):
    INFO = 'info'
    WARNING = 'warning'
    SUCCESS = 'success'
    TYPE_CHOICES = ((INFO, 'Info'), (WARNING, 'Warning'), (SUCCESS, 'Success'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=140)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# Create your models here.
