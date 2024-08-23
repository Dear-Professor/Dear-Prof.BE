from django.db import models
from django.conf import settings

class SentEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_email')
    title = models.CharField
    final_context = models.TextField()
    written_context = models.TextField()
    to_user = models.EmailField() # 교수님 메일
    created_at = models.DateTimeField()
    is_feedback = models.BooleanField(default=False)
    feedback = models.JSONField()
    subject = models.CharField(max_length=100) # 수업 이름

class ReceivedEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_email')
    title = models.CharField(max_length=100)
    context = models.TextField()
    from_user = models.EmailField() # 교수님 메일
    created_at = models.DateTimeField()
    response_to = models.ForeignKey(SentEmail, on_delete=models.CASCADE, related_name='response') # 뭐에 대한 답장인지