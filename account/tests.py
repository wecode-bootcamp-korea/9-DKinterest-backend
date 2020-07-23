from django.test import (
        TestCase,
        Client
)
from .models import Account
from .views import (
        SignUpView, 
        SignInView, 
        KakaoLogInView
)

from unittest.mock import (
        Mock, 
        patch, 
        MagicMock
)

import unittest
import json
import bcrypt
import requests
import jwt
import re
import bcrypt

client = Client()

class SignUpTest(TestCase):
    def setUp(self):
        Account.objects.create(
            email="yoojinyoojin@gmail.com", password="Asdf1234!!", age=31
        )

    def tearDown(self):
        Account.objects.all().delete()

    def test_post_signupview_success(self):
        client = Client()
        account = {
            "email": "yoojin@gmail.com",
            "password": "Asdf1234!!",
            "age": 31,
        }

        response = client.post(
            "/account/sign-up", json.dumps(account), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_signupview_existingemail(self):
        client = Client()
        account = {
            "email": "yoojinyoojin@gmail.com",
            "password": "Asdf1234!!",
            "age": 31,
        }

        response = client.post(
            "/account/sign-up", json.dumps(account), content_type="application/json"
        )
        self.assertEqual(response.json(), {"message": "Email Already exists"})
        self.assertEqual(response.status_code, 400)

    def test_post_signupview_invalidpassword(self):
        client = Client()
        account = {"email": "lyjlyj@gmail.com", "password": "1234", "age": 11}

        response = client.post(
            "/account/sign-up", json.dumps(account), content_type="application/json"
        )
        self.assertEqual(response.json(), {"message": "INVALID_PASSWORD"})
        self.assertEqual(response.status_code, 400)

    def test_post_signupview_invalidemail(self):
        client = Client()
        account = {"email": "yjyjyj", "password": "Asdf1234!!", "age": 23}
        response = client.post(
            "/account/sign-up", json.dumps(account), content_type="application/json"
        )
        self.assertEqual(response.json(), {"message": "INVALID_EMAIL"})
        self.assertEqual(response.status_code, 400)

    def test_post_signupview_notfound(self):
        client = Client()
        account = {"email": "aaaaa@gmail.com", "password": "Asdf1234!!", "age": 22}

        response = client.post(
            "/account/signup", json.dumps(account), content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_post_signupview_keyerror(self):
        client = Client()
        account = {
            "emaill": "yoojin@gmail.com",
            "password": "Asdf1234!!",
            "age": 31,
        }

        response = client.post(
            "/account/sign-up", json.dumps(account), content_type="application/json"
        )

        self.assertEqual(response.json(), {"message": "INVALID_KEYS"})
        self.assertEqual(response.status_code, 400)


class SignInTest(TestCase):
    def setUp(self):
        Account.objects.create(
            email="yoojinyoojin@gmail.com",
            password=bcrypt.hashpw(
                "Asdf1234!!".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            age=31,
        )

    def tearDown(self):
        Account.objects.all().delete()

    def test_post_signinview_success(self):
        client = Client()
        account = {
            "email": "yoojinyoojin@gmail.com",
            "password": "Asdf1234!!",
        }

        response = client.post(
            "/account/sign-in", json.dumps(account), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_signinview_fail(self):
        client = Client()
        account = {
            "email": "yoojinyoojin@gmail.com",
            "password": "Asdf1234!!!",
        }
        response = client.post(
            "/account/sign-in", json.dumps(account), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)

    def test_post_signinview_notfound(self):
        client = Client()
        account = {
            "email": "yoojinyoojin@gmail.com",
            "password": "Asdf1234!!",
        }
        response = client.post(
            "/account/sign-inn", json.dumps(account), content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)


class KakaoLogInViewTest(TestCase):
    @patch("account.views.requests")
    def test_kakao_signup_success(self, mocked_request):
        class MockedResponse:
            def json(self):
                user_info = {
                    "properties": {
                        "nickname": "yalsldf",
                        "profile_image": "https://i.pinimg.com/750x/b0/ae/92/b0ae920ae9e10a58c8b5176f3181bd73.jpg",
                    },
                    "kakao_account": {"email": "yooyo@gmail.com"},
                }
                return user_info

        mocked_request.get = MagicMock(return_value=MockedResponse())

        client = Client()

        #        header = {"HTTP_Authorization": "48cd941c76c1fb8f30ca5dcc60acafb7"}

        response = client.post("/account/kakao_login", content_type="applications/json")

        self.assertEqual(response.status_code, 200)

    @patch("account.views.requests")
    def test_kakao_signup_notfound(self, mocked_request):
        class MockedResponse:
            def json(self):
                user_info = {
                    "properties": {
                        "nickname": "yalsldf",
                        "profile_image": "https://i.pinimg.com/750x/b0/ae/92/b0ae920ae9e10a58c8b5176f3181bd73.jpg",
                    },
                    "kakao_account": {"email": "yooyo@gmail.com"},
                }
                return user_info

        mocked_request.get = MagicMock(return_value=MockedResponse())

        client = Client()

        header = {"HTTP_Authorization": "48cd941c76c1fb8f30ca5dcc60acafb7"}

        response = client.post(
            "/account/kakao_loginn", content_type="applications/json", **header
        )

        self.assertEqual(response.status_code, 404)

    @patch("account.views.requests")
    def test_kakao_login_badrequest(self, mocked_request):
        class MockedResponse:
            def json(self):
                user_info = {
                    "properties": {
                        "nickname": "yalsldf",
                        # "profile_image": "https://i.pinimg.com/750x/b0/ae/92/b0ae920ae9e10a58c8b5176f3181bd73.jpg",
                    },
                    "kakao_account": {"email": "yooyo@gmail.com"},
                }
                return user_info

        mocked_request.get = MagicMock(return_value=MockedResponse())

        client = Client()

        header = {"Authorization": "48cd941c76c1fb8f30ca5dcc60acafb7"}

        response = client.post(
            "/account/kakao_login", content_type="applications/json", **header
        )

        self.assertEqual(response.status_code, 400)


class InterestSaveViewTest(TestCase):
    def setUp(self):
        client = Client()
        Account.objects.create(
            id=59, email="dbwlsfda12@naver.com", password="Asdf1234!!", age=22
        )
        Interest.objects.create(id=2, title="강아지", image_url="toritori.jpg")

    def tearDown(self):
        AccountInterest.objects.all().delete()

    def test_interest_post_success(self):
        client = Client()
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRid2xzZmRhMTJAbmF2ZXIuY29tIn0.MtgXuZcXktWemphzR_Y5VZzx2c1gM5khTlAm8aF7uJs"
        }

        account_interest = {"account_id": 59, "interestId": [2]}

        response = client.post(
            "/account/interest",
            json.dumps(account_interest),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 200)

    def test_interest_post_fail(self):
        client = Client()
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRid2xzZmRhMTJAbmF2ZXIuY29tIn0.MtgXuZcXktWemphzR_Y5VZzx2c1gM5khTlAm8aF7uJs"
        }

        # account_interest = {"account_id": 59, "interestId": [2]}
        account_interest = {"interestId": []}

        response = client.post(
            "/account/interest",
            json.dumps(account_interest),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)

    def test_interest_badrequest(self):
        client = Client()
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRid2xzZmRhMTJAbmF2ZXIuY29tIn0.MtgXuZcXktWemphzR_Y5VZzx2c1gM5khTlAm8aF7uJs"
        }

        account_interest = {"account_id": 59, "interestId": [2]}

        response = client.post(
            "/account/interests",
            json.dumps(account_interest),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 404)
