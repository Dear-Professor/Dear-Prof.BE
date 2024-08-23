from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SentMailViewset

# Router 설정
router = DefaultRouter()
router.register(r'sentmail', SentMailViewset)

urlpatterns = [
    path('', include(router.urls)),
]
