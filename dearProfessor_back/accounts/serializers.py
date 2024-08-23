from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'grade', 'studentId', 'major', 'school']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            grade=validated_data['grade'],
            studentId=validated_data['studentId'],
            major=validated_data['major'],
            school=validated_data['school']
        )
        return user
