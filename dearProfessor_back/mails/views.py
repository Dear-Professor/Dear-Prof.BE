from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, generics

from . serializers import *

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
            serializer.save()
            
            # 이메일 발송
            send_mail(
                subject=title,  # 이메일의 실제 제목
                message=final_context,
                from_email=user.email,
                recipient_list=[to_user]
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    