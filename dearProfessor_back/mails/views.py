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


from django.shortcuts import get_object_or_404

    
# 메일 보내기. 
class SendEmailView(APIView):

    def post(self, request):
        serializer = SentEmailSerializer(data=request.data)
        if serializer.is_valid():
            from_email = serializer.validated_data['from_email']
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            send_mail(subject, message, from_email, [to_email])

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


  