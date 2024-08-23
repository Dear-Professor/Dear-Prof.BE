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
        instance = serializer.save(user=self.request.user)

        # 먼저 유효성 검사를 통과한 데이터를 가져옵니다.
        validated_data = serializer.validated_data

        prompt = (
            f"\n"
            f"너는 사용자가 입력한 내용을 기반으로 대학생이 교수님에게 보낼 메일을 검토해주는 역할이야. 문법과 양식, 격식 차린 말투인지를 확인해주면 돼."
            f"목적 :학생인 사용자가 교수님에게 의도에 맞는 메일을 적절한 양식과 올바른 문법으로 보내는 걸 도와주기 위함이야.\n"
            f"1. 말투는 ‘-합니다’체를 써. 사용자인 발신자가 대학생이라 주로 20대고, 수신자는 대학교 교수님인 점을 참고하여 예의바르고 사무적으로 쓰는 게 좋아. 구어체는 지양해줘.\n"
            f"2. 첫번째는 인삿말을 만드는 게 좋아.\n"
            f"3. 그 다음은 자신의 [학과], [학번], [이름]으로 자기소개를 해야 해.\n"
            f"4. 인사가 끝났으면 메일을 쓴 목적을 써야 하는데 사용자가 작성한 내용의 목적을 토대로 다듬어서 작성해줘. 생략되는 내용은 되도록은 없었으면 좋겠어. 형식은 ‘(목적) 관련으로 메일 드립니다.’ 혹은 ‘(목적) 관련으로 메일을 쓰게 되었습니다.’ 같은 느낌이었으면 좋겠어.\n"
            f"5. 목적 작성 후 상세 내용 작성으로, 두괄식으로 작성해줬으면 좋겠어.\n"
            f"6. 메일 내용이 다 끝났으면 끝맺음 인사를 간결하게 쓰고 문단을 두개 띄운 다음 ‘감사합니다.’ 를 넣고 ‘[학과] [학번] [이름] 올림’ 이라고 써줬으면 좋겠어.\n"
            f"7. 이모지나 특수 기호의 사용은 자제해줬으면 좋겠어. 사용자가 내용에 썼다면 되도록 생략해줘.\n"
            f"8. 사용자의 입력 내용이 너무 짧다면 사용자가 채워 넣을 수 있게 빈칸으로 만들어서 넣어줘. 예를 들어 ‘저는 [생각 중인 진로]로 갈까 고민 중에 있어 교수님의 의중을 여쭙고 싶습니다.’ 이런식으로 사용자가 채워넣어야 할 부분을 구체적이고 입력하기 쉽게 작성해줘.{subject}이 없다면 그 부분은 생략해줘.\n"
            f"9.여러 사용자가 메일 피드백을 받을 테니까 예시와 너무 똑같이 피드백 주지 말고 양식은 유지하되, 단어와 어휘는 조금씩 바꿔서 작성해줘.\n"
            f"입력 정보: [학번]:{validated_data.get('studentId')}, [학과]:{validated_data.get('major')},[이름]:{validated_data.get('name')},[강의명]:{instance.subject}"
            f"위의 입력정보를 아래 템플릿에 반영하여서 글을 작성해줘"
            f"예시: 사용자 입력 내용: 응용통계학과 2022122069 김지민인데여, 통계학과 진로가 궁금해요.\n"
            f"피드백 메일 내용: "
            f"\n"
            f"안녕하세요 교수님. 저는 응용통계학과 2022122069 김지민입니다.\n"
            f"진로 선택에 대한 조언을 구하고자 메일을 드립니다. 저는 현재 [생각 중인 진로]로 갈까 고민 중에 있으며, 교수님의 조언을 듣고 싶어 이렇게 메일을 쓰게 되었습니다.\n"
            f"응용통계학과를 졸업한 후에는 다양한 진로가 있을 수 있는 것으로 알고 있습니다. 예를 들어, 데이터 분석, 통계 컨설팅, 연구, 또는 학계로 진출하는 길 등(사용자의 학과 관련 진로 예시들을 써줘)이 있는 걸로 알고 있습니다. 각 분야의 장단점이나 요구되는 역량에 대해 교수님의 경험을 바탕으로 조언을 주시면 큰 도움이 될 것입니다. 또한, 이와 관련된 자료나 추천해주실 만한 참고문헌이 있다면 알려주시면 감사하겠습니다.\n"
            f"\n"
            f"답변 주시면 감사하겠습니다.\n"
            f"\n"
            f"감사합니다."
            f"\n"
            f"2022122069 김지민 올림”"
            f"사용자 입력 내용: 컴퓨터과학과 2024122069 김컴과인데, 자료구조 수업 증원해주세요 안그러면 더 심화 내용을 못 들어요 제발요ㅠㅠ\n"
            f"피드백 메일 내용:"
            f"“[교수님 성함] 교수님께,"
            f"\n"
            f"안녕하세요. 저는 컴퓨터과학과 2024122069 김컴과입니다."
            f"\n"
            f"자료구조 수업의 증원 요청과 관련하여 메일을 드립니다. 저는 이번에 ‘자료구조’ 수업 수강 신청을 했지만 현재 해당 수업이 수강 인원 초과로 인해 수강이 어려운 상황입니다. 하지만 이 과목은 다수의 과목들의 선수 과목으로, 이 수업을 수강하지 못할 경우, 향후 더 심화된 내용을 배우는 데 어려움이 있을 것 같습니다. 따라서, 이번 학기에 교수님의 ‘자료구조’ 수업을 꼭 듣고 싶어 수업의 증원을 고려해주실 수 있는지 여쭙고 싶습니다. 제 상황을 고려하시어 긍정적인 답변을 주시면 대단히 감사하겠습니다."
            f"\n"
            f"답변 주시면 감사하겠습니다."
            f"\n"
            f"감사합니다."
            f"\n"
            f"2024122069 김컴과 올림”"
            f"\n"
        )
        
        # 여기서 useGPT 함수를 호출하여 final_context를 생성합니다.
        final_context = useGPT(prompt + instance.written_context)  # useGPT 함수는 정의된 함수입니다.
        
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


class MailViewsetOptions(ModelViewSet):

    queryset = SentEmail.objects.all()
    serializer_class = SentEmailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        # 먼저 유효성 검사를 통과한 데이터를 가져옵니다.
        validated_data = serializer.validated_data

        # 모델 인스턴스를 먼저 저장하여 기본 데이터를 채웁니다.
        instance = serializer.save(user=self.request.user)
        
        prof_email = self.request.data.get('prof_email')
        validated_data['to_user'] = prof_email
        instance.to_user = prof_email

        subject = self.request.data.get('subject')
        purpose = self.request.data.get('purpose')

        prompt = (
            f"너는 사용자가 입력한 내용을 기반으로 대학생이 교수님께 보낼 메일을 대신 작성해주는 역할이야. 문법과 양식, 격식 차린 말투를 올바르게 해서 작성해주면 돼. 학생인 사용자가 교수님께 의도에 맞는 메일을 적절한 양식과 올바른 문법으로 보내는 걸 도와주기 위함이야."
            f"1. 말투는 ‘-합니다’체를 써. 사용자인 발신자가 대학생이라 주로 20대고, 수신자는 대학교 교수님인 점을 참고하여 예의바르고 사무적으로 쓰는 게 좋아. 구어체는 지양해줘.\n"
            f"2. 첫번째는 인삿말을 만드는 게 좋아.\n"
            f"3. 그 다음은 자신의 [학과], [학번], [이름]으로 자기소개를 해야 해.\n"
            f"4. 인사가 끝났으면 메일을 쓴 목적을 써야 하는데 사용자가 선택한 목적을 토대로 다듬어서 작성해줘. 생략되는 내용은 되도록은 없었으면 좋겠어. 형식은 ‘[(목적)] 관련으로 메일 드립니다.’ 혹은 ‘[(목적)] 관련으로 메일을 쓰게 되었습니다.’ 같은 느낌이었으면 좋겠어.\n"
            f"5. 목적 작성 후 상세 내용 작성으로, 두괄식으로 작성해줬으면 좋겠어.\n"
            f"6. 메일 내용이 다 끝났으면 끝맺음 인사를 간결하게 쓰고 문단을 두개 띄운 다음 ‘감사합니다.’ 를 넣고 ‘[학과] [학번] [이름] 올림’ 이라고 써줬으면 좋겠어.\n"
            f"7. 이모지나 특수 기호의 사용은 자제해줬으면 좋겠어. 사용자가 내용에 썼다면 되도록 생략해줘.\n"
            f"8. 사용자의 입력 내용이 너무 짧다면 사용자가 채워 넣을 수 있게 빈칸으로 만들어서 넣어줘. 예를 들어 ‘저는 [생각 중인 진로]로 갈까 고민 중에 있어 교수님의 조언을 구하고 싶습니다.’ 이런식으로 사용자가 채워넣어야 할 부분을 구체적이고 입력하기 쉽게 작성해줘. 강의명이 없다면 그 부분은 생략해줘.\n"
            f"9.여러 사용자가 메일 피드백을 받을 테니까 예시와 너무 똑같이 피드백 주지 말고 양식은 유지하되, 단어와 어휘는 조금씩 바꿔서 작성해줘.\n"
            f"입력 정보: [학번]:{validated_data.get('studentId')}, [학과]:{validated_data.get('major')},[이름]:{validated_data.get('name')},[강의명]:{subject},[카테고리]:{purpose}"
            f"예시: 사용자 입력 내용: 사용자 선택 및 입력 내용: 응용통계학과, [학번], [이름], [강의명], [카테고리:진로 고민]\n"
            f"입력 정보를 아래 메일 내용에 반영해서 작성해줘"
            f"피드백 메일 내용: "
            f"“교수님께,\n"
            f"\n"
            f"안녕하세요. 저는 응용통계학과 2022122069 김지민입니다.\n"
            f"진로 선택에 대한 조언을 구하고자 메일을 드립니다. 저는 현재 [생각 중인 진로]로 갈까 고민 중에 있으며, 교수님의 조언을 듣고 싶어 이렇게 메일을 쓰게 되었습니다.\n"
            f"응용통계학과를 졸업한 후에는 다양한 진로가 있을 수 있는 것으로 알고 있습니다. 예를 들어, 데이터 분석, 통계 컨설팅, 연구, 또는 학계로 진출하는 길 등(사용자의 학과 관련 진로 예시들을 써줘)이 있는 걸로 알고 있습니다. 각 분야의 장단점이나 요구되는 역량에 대해 교수님의 경험을 바탕으로 조언을 주시면 큰 도움이 될 것입니다. 또한, 이와 관련된 자료나 추천해주실 만한 참고문헌이 있다면 알려주시면 감사하겠습니다.\n"
            f"\n"
            f"답변 주시면 감사하겠습니다.\n"
            f"\n"
            f"감사합니다."
            f"\n"
            f"2022122069 김지민 올림”"
            f"사용자 입력 내용: 컴퓨터과학과 2024122069 김컴과인데, 자료구조 수업 증원해주세요 안그러면 더 심화 내용을 못 들어요 제발요ㅠㅠ\n"
            f"피드백 메일 내용:"
            f"“존경하는 교수님께,"
            f"\n"
            f"안녕하세요. 저는 컴퓨터과학과 2024122069 김컴과입니다."
            f"\n"
            f"자료구조 수업의 증원 요청과 관련하여 메일을 드립니다. 저는 이번에 ‘자료구조’ 수업 수강 신청을 했지만 현재 해당 수업이 수강 인원 초과로 인해 수강이 어려운 상황입니다. 하지만 이 과목은 다수의 과목들의 선수 과목으로, 이 수업을 수강하지 못할 경우, 향후 더 심화된 내용을 배우는 데 어려움이 있을 것 같습니다. 따라서, 이번 학기에 교수님의 ‘자료구조’ 수업을 꼭 듣고 싶어 수업의 증원을 고려해주실 수 있는지 여쭙고 싶습니다. 제 상황을 고려하시어 긍정적인 답변을 주시면 대단히 감사하겠습니다."
            f"\n"
            f"답변 주시면 감사하겠습니다."
            f"\n"
            f"감사합니다."
            f"\n"
            f"2024122069 김컴과 올림”"
        )

        
        # 여기서 useGPT 함수를 호출하여 final_context를 생성합니다.
        final_context = useGPT(prompt)  # useGPT 함수는 정의된 함수입니다.
        
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
    


    #yeeun
    #받은 메일 리스트/상세조회

class ReceiveMailViewset(ModelViewSet):
    queryset = ReceivedEmail.objects.all()
    serializer_class = ReceiveEmailViewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False,methods=['get'] ,url_path='list_receiveMail')
    def list_receivemail(self,request,user_id=None):
        user_id=int(request.query_params.get('user_id'))
        authenticated_user_id = request.user.id
        if not user_id:
            return Response({"status": "error", "message": "month_id is required"}, status=400)
        
        if user_id != authenticated_user_id :
            return Response({"status": "error", "message": "훔쳐보지마~!"}, status=401)
        
        queryset = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
        
     # #받은 메일 상세 보기
    @action(detail=False,methods=['get'] ,url_path='detail_receiveMail')
    def detail_receivemail(self,request,user_id=None,mail_id=None):
        user_id=int(request.query_params.get('user_id'))
        mail_id = request.query_params.get('mail_id')
        authenticated_user_id = request.user.id
        if not user_id:
            return Response({"status": "error", "message": "month_id is required"}, status=400)
        
        if user_id != authenticated_user_id :
            return Response({"status": "error", "message": "훔쳐보지마~!"}, status=401)
        
        if not mail_id:
            return Response({"status": "error", "message": "mail_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        mail = get_object_or_404(ReceivedEmail,id=mail_id,user_id=user_id)
        serializer = self.get_serializer(mail)
        return Response({"status":"success","data":  serializer.data}, status=status.HTTP_200_OK)



  