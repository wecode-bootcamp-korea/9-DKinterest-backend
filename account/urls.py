from django.urls import path

from django.urls import path, include

from .views import (
    SignUpView,
    SignInView,
    KakaoLogInView
)

urlpatterns = [
    path("/sign-up", SignUpView.as_view()),
    path("/sign-in", SignInView.as_view()),
    path("/kakao_login", KakaoLogInView.as_view()),
]
