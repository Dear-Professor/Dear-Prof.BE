from django.db import models
from django.conf import settings

# Create your models here.
class SentEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_email')
    title = models.CharField
    final_context = models.TextField()
    written_context = models.TextField()
    to_user = models.EmailField()
    created_at = models.DateTimeField()
    is_feedback = models.BooleanField(default=False)
    feedback = models.JSONField()

class ReceivedEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_email')
    title = models.CharField
    final_context = models.TextField()
    from_user = models.EmailField()
    created_at = models.DateTimeField()
    response_to = models.ForeignKey(SentEmail, on_delete=models.CASCADE, related_name='response')