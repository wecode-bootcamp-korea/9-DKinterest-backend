import jwt
import requests
from account.models import Account
from django.http import (
    HttpResponse, 
    JsonResponse
)
from dkinterest.settings import SECRET_KEY, ALGORITHM


def decorator_login(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get("Authorization", None)
            payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
            user = Account.objects.get(email=payload["email"])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({"Error Message": "INVALID_TOKEN"}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({"Error Message": "ID DOES NOT EXIST"}, status=400)
        return func(elf, request, *args, **kwargs)

    return wrapper
s
