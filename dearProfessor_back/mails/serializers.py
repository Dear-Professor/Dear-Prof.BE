from rest_framework import serializers

from .models import *

class SendSerializer(serializers.Serializer):
    name = serializers.ReadOnlyField(source = 'user.name')
    from_email = serializers.ReadOnlyField(source = 'user.email')
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

    class Meta:
        model = SentEmail
        fields = []
