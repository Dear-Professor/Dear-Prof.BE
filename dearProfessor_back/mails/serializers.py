from rest_framework import serializers

from .models import *

class SentEmailSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = 'user.name')
    from_email = serializers.ReadOnlyField(source = 'user.email')
    user_id = serializers.ReadOnlyField(source = 'user.id')
    studentId = serializers.ReadOnlyField(source = 'user.studentId')
   
    class Meta:
        model = SentEmail
        fields = [
            'id', 'user_id', 'name', 'from_email', 'title', 
            'written_context', 'final_context', 'to_user', 
            'created_at', 'is_feedback', 'feedback', 'subject', 'studentId'
        ]
    
class ReceivedEmailSerializer(serializers.ModelSerializer):
    response_to = serializers.ReadOnlyField(source='id')

    class Meta:
        model = SentEmail
        fields = [
            'response_to', 'id', 'user', 'title', 
            'final_context', 'from_email', 'created_at'
        ]


#yeeun
class SentEmailViewSerializer(serializers.ModelSerializer):
    # `user` 필드에서의 값을 직접 가져오는 것이 아니라, `SentEmail` 모델의 필드만을 포함
    class Meta:
        model = SentEmail
        fields = '__all__'

#yeeun
class ReceiveEmailViewSerializer(serializers.ModelSerializer):
    # `user` 필드에서의 값을 직접 가져오는 것이 아니라, `SentEmail` 모델의 필드만을 포함
    class Meta:
        model = ReceivedEmail
        fields = '__all__'