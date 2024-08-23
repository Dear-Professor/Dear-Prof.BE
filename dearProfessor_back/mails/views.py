from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, viewsets, generics

from . serializers import *

# class SentEmailListView(viewsets.ViewSet):
    

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
