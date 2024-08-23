from django.urls import path,include
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('',include('dj_rest_auth.urls')),
    path('',include('dj_rest_auth.registration.urls')),
]
