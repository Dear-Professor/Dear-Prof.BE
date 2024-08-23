from django.db import models
from django.conf import settings

class SentEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_email')
    title = models.CharField(max_length=150)
    final_context = models.TextField(blank=True, null=True, default="") # feedback
    written_context = models.TextField(blank=True, null=True, default="")
    to_user = models.EmailField(blank=True, null=True, default="anthony0102@naver.com") # 교수님 메일
    created_at = models.DateTimeField(auto_now_add=True)
    is_feedback = models.BooleanField(default=False)
    feedback = models.JSONField(default=dict)
    subject = models.CharField(blank=True, null=True, default='', max_length=100) # 수업 이름

class ReceivedEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_email')
    title = models.CharField(max_length=100)
    context = models.TextField()
    from_user = models.EmailField() # 교수님 메일
    created_at = models.DateTimeField()
    response_to = models.ForeignKey(SentEmail, on_delete=models.CASCADE, related_name='response') # 뭐에 대한 답장인지