import re
import bcrypt
import requests
import jwt
import json
import re

from django.views.decorators.csrf       import csrf_exempt
from django.core.exceptions             import ObjectDoesNotExist
from django.http                        import (
    JsonResponse,
    HttpResponse
)
from django.http                        import 
from django.views                       import View

from .utils                             import decorator_login
from dkinterest.settings                import (
        SECRET_KEY, 
        ALGORITHM
)
from account.models                     import Account

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_validation = re.compile(
            "^\S[a-zA-Z0-9+-_.]{4,28}\S@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )
        password_validation = re.compile(
           "^(?=.{10,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$"
        )

        try:
            if Account.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "Email Already Exists"}, status=400)

            if email_validation.match(data["email"]):
                if password_validation.match(data["password"]):
                    password = bcrypt.hashpw(
                        data["password"].encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    Account.objects.create(
                        email       =   data["email"],
                        password    =   password,
                        age         =   data["age"]
                    )
                    return HttpResponse(status=200)

                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)

            return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class SignInView(View):
    def post(self, request):
        data    =   json.loads(request.body)
        try:
            if Account.objects.filter(email=data["email"]).exists():
                account     =   Account.objects.get(email=data["email"])

                if bcrypt.checkpw(
                    data["password"].encode("utf-8"), account.password.encode("utf-8")
                ):
                    token   =   jwt.encode(
                        {"email": account.email}, SECRET_KEY, algorithm=ALGORITHM
                    )
                    return JsonResponse({"token": token.decode("utf-8")}, status=200)

                return HttpResponse(status=401)

            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status=400)


class KakaoLogInView(View):
    def post(self, request):
        access_token        =       request.headers.get("Authorization", None)
        kakao_url           =       "https://kapi.kakao.com/v2/user/me"
        headers             =       {"Authorization": f"Bearer {access_token}"}
        request_kakao_info  =       requests.get(kakao_url, headers=headers)
        kakao_user_info     =       request_kakao_info.json()
        kakao_user_email    =       kakao_user_info["kakao_account"]["email"]
        kakao_user_nickname =       kakao_user_info["properties"]["nickname"]

        if not (Account.objects.filter(email=kakao_user_email).exists()):
            account         =       Account.objects.create(
                email       =       kakao_user_email,
                nickname    =       kakao_user_nickname,
            )
            access_token    =       jwt.encode(
                {"email": account.email}, SECRET_KEY, ALGORITHM
            ).decode("utf-8")
            return JsonResponse(
                {
                    "email": kakao_user_email,
                    "nickname": kakao_user_nickname,
                },
                status=200,
            )
        access_token    =   jwt.encode(
            {"email": kakao_user_email}, SECRET_KEY, ALGORITHM
        ).decode("utf-8")
        return JsonResponse({"access_token" : access_token}, status=200)

class KakaoLogInView(View):
    def get(self, request):
        kakao_id_token          =       request.headers.get("Authorization", None)

        if kakao_id_token is None:
            return JsonResponse({"message": "MISSING_KAKAO_TOKEN"}, status=400)
        kakao_url               =       "https://kapi.kakao.com/v2/user/me"
        headers                 =       {"Authorization": f"Bearer {token}"}
        request_kakao_info      =       requests.get(kakao_url, headers=headers)
        kakao_user_info         =       request_kakao_info.json()
        kakao_user_email        =       kakao_user_info["kakao_account"]["email"]

        if Account.objects.filter(email=kakao_user_email).exists():
            token = jwt.encode(
                {"email": kakao_user_email}, SECRET_KEY, ALGORITHM
            ).decode("utf-8")

            return JsonResponse({"token": token}, status=200)

        return JsonResponse({"message" : "SIGN-UP NEEDED"}, status=400) 
