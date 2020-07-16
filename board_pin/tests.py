import json

from django.test      import TestCase, Client
from django.core      import serializers

from board_pin.models import (
    Pin,
    Board,
    BoardPin
)

from account.models   import (
    SocialPlatform,
    Gender,
    Region,
    Language,
    Account,
    Interest
)
from account.utils    import decorator_login

from unittest.mock    import patch, MagicMock
from io               import BytesIO

class PinCreateTest(TestCase):
    def setUp(self):
        SocialPlatform.objects.create(
            id   = 1,
            name = 'Pinterest'
        )
        Gender.objects.create(
            id   = 1,
            name = '남성'
        )
        Region.objects.create(
            id   = 1,
            name = '대한민국'
        )
        Language.objects.create(
            id       = 1,
            language = '한국어'
        )
        Account.objects.create(
            id              = 1,
            name            = 'kim',
            email           = 'dgk2481@gmail.com',
            image_url       = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            gender          = Gender.objects.get(id=1),
            region          = Region.objects.get(id=1),
            language        = Language.objects.get(id=1),
            social_platform = SocialPlatform.objects.get(id=1),
            follower_number = 12
        )
        Interest.objects.create(
            id        = 1,
            title     = '예술',
            image_url = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg'
        )

    def tearDown(self):
        SocialPlatform.objects.all().delete()
        Gender.objects.all().delete()
        Region.objects.all().delete()
        Language.objects.all().delete()
        Account.objects.all().delete()
        Interest.objects.all().delete()

    def test_pin_create_success(self):
        client = Client()
        img = BytesIO(b'randomImage')
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazI0ODFAZ21haWwuY29tIn0.Zgv2dYLUfzfcJxIFgboJQ8lRYpFiDOAxcwrs4BmTuls"}
        pin = {
            'filename' : img,
            'title'    : 'hello',
            'detail'   : 'hi',
            'link'     : 'www.naver.com',
        }
        response = client.post('/boardpin/pincreate', pin, **headers)
        self.assertEqual(response.status_code, 200)