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
from .models import SentEmail
from .chatGPT_api import useGPT
from .post_fetch_mail import *

from django.shortcuts import get_object_or_404

    
class MailViewset(ModelViewSet):
    queryset = SentEmail.objects.all()
    serializer_class = SentEmailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 모델 인스턴스를 먼저 저장하여 기본 데이터를 채웁니다.
        instance = serializer.save()
        
        # 여기서 useGPT 함수를 호출하여 final_context를 생성합니다.
        final_context = useGPT(instance.written_context)  # useGPT 함수는 정의된 함수입니다.
        
        # 생성된 final_context를 인스턴스에 추가하고 다시 저장합니다.
        instance.final_context = final_context
        instance.save()
        
        return instance
    
    def update(self, request, *args, **kwargs):
        # 기존 인스턴스를 가져옵니다.
        instance = self.get_object()

        # 사용자가 final_context만 수정할 수 있도록 제한합니다.
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # final_context만 변경된 내용으로 업데이트합니다.
        if 'final_context' in serializer.validated_data:
            instance.final_context = serializer.validated_data['final_context']
            instance.save()

        post_emails(instance.to_user, instance.title, instance.final_context)

        # 성공적인 응답을 반환합니다.
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # 특정 SentEmail 인스턴스를 가져옵니다.
        instance = self.get_object()
        
        # final_context만 반환합니다.
        return Response({"final_context": instance.final_context})



#보낸 메일 리스트/상세 조회
class SentMailViewset(ModelViewSet):
    queryset = SentEmail.objects.all()  # 기본 쿼리셋 정의
    serializer_class = SentEmailViewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    #보낸메일리스트 가져오기 
    @action(detail=False,methods=['get'] ,url_path='list_sentMail')
    def list_sentmail(self,request,user_id=None):
        user_id=int(request.query_params.get('user_id'))
        authenticated_user_id = request.user.id
        if not user_id:
            return Response({"status": "error", "message": "month_id is required"}, status=400)
        
        if user_id != authenticated_user_id :
            return Response({"status": "error", "message": "훔쳐보지마~!"}, status=401)
        
        queryset = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
    
    # #보낸 메일 상세 보기
    @action(detail=False,methods=['get'] ,url_path='detail_sentMail')
    def detail_sentmail(self,request,user_id=None,mail_id=None):
        user_id=int(request.query_params.get('user_id'))
        mail_id = request.query_params.get('mail_id')
        authenticated_user_id = request.user.id
        if not user_id:
            return Response({"status": "error", "message": "month_id is required"}, status=400)
        
        if user_id != authenticated_user_id :
            return Response({"status": "error", "message": "훔쳐보지마~!"}, status=401)
        
        if not mail_id:
            return Response({"status": "error", "message": "mail_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        mail = get_object_or_404(SentEmail,id=mail_id,user_id=user_id)
        serializer = self.get_serializer(mail)
        return Response({"status":"success","data":  serializer.data}, status=status.HTTP_200_OK)


  