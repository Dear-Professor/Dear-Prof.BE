from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SentMailViewset, MailViewset

# Router 설정
router = DefaultRouter()
router.register(r'sentmail', SentMailViewset)

# mail 생성, 업데이트, 조회
Mail_urls = MailViewset.as_view({
        'post' : 'create',
        'get' : 'retrieve',
        'put' : 'update'
    }
)




urlpatterns = [
    path('', include(router.urls)),
    path('mail/', Mail_urls),
]
