from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SentMailViewset, MailViewset, MailViewsetOptions

# Router 설정
router = DefaultRouter()
router.register(r'sentmail', SentMailViewset)

# mail 생성, 업데이트, 조회
Mail_urls = MailViewset.as_view({
        'post' : 'create',
    }
)

Mail_urls_detail = MailViewset.as_view({

        'get' : 'retrieve',
        'put' : 'update'
        
})
    
Mail_option_urls = MailViewsetOptions.as_view({
        'post' : 'create',
    }
)

Mail_option_urls_detail = MailViewset.as_view({

        'get' : 'retrieve',
        'put' : 'update'
        
})

urlpatterns = [
    path('', include(router.urls)),
    path('typeAll/', Mail_urls),
    path('typeAll/<int:pk>/', Mail_urls_detail),
    path('selectOptions/', Mail_option_urls),
    path('selectOptions/<int:pk>/', Mail_option_urls_detail),
]
