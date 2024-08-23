from django.shortcuts import render
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, generics
from rest_framework.viewsets import ModelViewSet
from . serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class SentEmailListView(viewsets.ViewSet):
    queryset = SentEmail.objects.all
    serializer_class = SentEmailSerializer
    
class SendEmailView(APIView):

    def post(self, request):
        # 사용자의 정보를 요청 데이터에서 가져오기
        user = request.user
        to_user = request.data.get('to_user')
        subject = request.data.get('subject', 'No Subject')  # 과목명
        title = request.data.get('title', 'No Title')  # 이메일 제목
        final_context = request.data.get('final_context', '')

        # SentEmail 객체 생성
        email_data = {
            # 'user': user.id,
            # 'name': user.name,
            'title': title,  # 이메일 제목
            'final_context': final_context,
            'to_user': to_user,
            # 'is_feedback': request.data.get('is_feedback', False),
            # 'feedback': request.data.get('feedback', ''),
            # 'subject': subject  # 과목명 저장
        }

        serializer = SentEmailSerializer(data=email_data)
        
        if serializer.is_valid():
            from_email = serializer.validated_data['from_email']
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            send_mail(subject, message, from_email, [to_email])

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
