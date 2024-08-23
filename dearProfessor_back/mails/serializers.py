from rest_framework import serializers

from .models import *

class SentEmailSerializer(serializers.Serializer):
    name = serializers.ReadOnlyField(source = 'user.name')
    from_email = serializers.ReadOnlyField(source = 'user.email')
    grade = serializers.ReadOnlyField(source = 'user.grade')
    studentId = serializers.ReadOnlyField(source = 'user.studentId')
    major = serializers.ReadOnlyField(source = 'user.major')
    school = serializers.ReadOnlyField(source = 'user.school')

    class Meta:
        model = SentEmail
        fields = ['id','user','name','from_email','grade','studentId','major','school',
                  'title','written_context','final_context','to_user','created_at','is_feedback','feedback','subject']

class ReceivedEmailSerializer(serializers.Serializer):
    response_to = serializers.ReadOnlyField(source = 'sentmail.id')

    class Meta:
        model = SentEmail
        fields = ['response_to','id','user','title','context','from_user','created_at']
