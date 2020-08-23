from django.urls import path, include

from .views import (
    SignUpView, SignInView, KakaoLogInView, InterestSaveView
)

urlpatterns = [
    path("/sign-up", SignUpView.as_view()),
    path("/sign-in", SignInView.as_view()),
    path("/kakao_login", KakaoLogInView.as_view()),
    path("/interest", InterestSaveView.as_view()),
]