import json

from django.test      import (
    TestCase,
    Client
)
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

from unittest.mock    import (
    patch,
    MagicMock
)

from io               import BytesIO

class PinDetailTest(TestCase):
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
            email           = 'dgk089@gmail.com',
            image_url       = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            gender          = Gender.objects.get(id=1),
            region          = Region.objects.get(id=1),
            language        = Language.objects.get(id=1),
            social_platform = SocialPlatform.objects.get(id=1),
            follower_number = 12
        )
        Board.objects.create(
            id      = 1,
            name    = 'board1',
            account = Account.objects.get(id=1)
        )
        Pin.objects.create(
            id               = 1,
            internal_account = Account.objects.get(id=1),
            external_account = Account.objects.get(id=1),
            image_url        = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            title            = 'hello',
            detail           = 'hi',
            link             = 'https://twitter.com/',
        )
        BoardPin.objects.create(
            id    = 1,
            board = Board.objects.get(id=1),
            pin   = Pin.objects.get(id=1)
        )
    
    def tearDown(self):
        SocialPlatform.objects.all().delete()
        Gender.objects.all().delete()
        Region.objects.all().delete()
        Language.objects.all().delete()
        Account.objects.all().delete()
        Board.objects.all().delete()
        Pin.objects.all().delete()
        BoardPin.objects.all().delete()

    def test_pindetail_get_success(self):
        client = Client()
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazA4OUBnbWFpbC5jb20ifQ.vXF4ThqZuqYA9Wl3NKEBIdFhqJNyadO5X3pSJFIUF8Q"}
        response = client.get('/boardpin/pin?pin_id=1', **headers, content_type="application/json")
        self.assertEqual(response.json(),{
            'pin' : [{
                'internalAccount'    : 'kim',
                'internalAccountImg' : 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
                'externalAccount'    : 'kim',
                'externalAccountImg' : 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
                'imgUrl'             : 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
                'title'              : 'hello',
                'detail'             : 'hi',
                'link'               : 'https://twitter.com/',
                'boardName'          : 'board1',
                'followNumber'       : 12
            }]
        }
        )
        self.assertEqual(response.status_code, 200)

    def test_pindetail_get_not_found(self):
        client = Client()
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazA4OUBnbWFpbC5jb20ifQ.vXF4ThqZuqYA9Wl3NKEBIdFhqJNyadO5X3pSJFIUF8Q"}
        response = client.get('/boardpin/pin?pin_id=200', **headers, content_type="application/json")
        self.assertEqual(response.json(),{
            'message' : 'NO_PIN'
        })
        self.assertEqual(response.status_code, 400)

class MypageAccountTest(TestCase):
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
            email           = 'dgk089@gmail.com',
            image_url       = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            gender          = Gender.objects.get(id=1),
            region          = Region.objects.get(id=1),
            language        = Language.objects.get(id=1),
            social_platform = SocialPlatform.objects.get(id=1),
            follower_number = 12
        )

    def tearDown(self):
        SocialPlatform.objects.all().delete()
        Gender.objects.all().delete()
        Region.objects.all().delete()
        Language.objects.all().delete()
        Account.objects.all().delete()
        Interest.objects.all().delete()

    def test_mypage_account_get_success(self):
        client = Client()
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazA4OUBnbWFpbC5jb20ifQ.vXF4ThqZuqYA9Wl3NKEBIdFhqJNyadO5X3pSJFIUF8Q"}
        response = client.get('/boardpin/mypageaccount', **headers, content_type="application/json")
        self.assertEqual(response.json(),{
            'account' : {
                'accountId'     : 1,
                'accountName'   : 'kim',
                'accountImage'  : 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
                'accountFollow' : 12,
            }
        })
        self.assertEqual(response.status_code, 200)

class MypageBoardTest(TestCase):
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
            email           = 'dgk089@gmail.com',
            image_url       = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            gender          = Gender.objects.get(id=1),
            region          = Region.objects.get(id=1),
            language        = Language.objects.get(id=1),
            social_platform = SocialPlatform.objects.get(id=1),
            follower_number = 12
        )
        Board.objects.create(
            id      = 1,
            name    = 'board1',
            account = Account.objects.get(id=1)
        )
        Pin.objects.create(
            id               = 1,
            internal_account = Account.objects.get(id=1),
            external_account = Account.objects.get(id=1),
            image_url        = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            title            = 'hello',
            detail           = 'hi',
            link             = 'https://twitter.com/',
        )
        BoardPin.objects.create(
            id    = 1,
            board = Board.objects.get(id=1),
            pin   = Pin.objects.get(id=1)
        )

    def tearDown(self):
        SocialPlatform.objects.all().delete()
        Gender.objects.all().delete()
        Region.objects.all().delete()
        Language.objects.all().delete()
        Account.objects.all().delete()
        Board.objects.all().delete()
        Pin.objects.all().delete()
        BoardPin.objects.all().delete()

    def test_mypage_board_get_success(self):
        client = Client()
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazA4OUBnbWFpbC5jb20ifQ.vXF4ThqZuqYA9Wl3NKEBIdFhqJNyadO5X3pSJFIUF8Q"}
        response = client.get('/boardpin/mypageboard', **headers, content_type="application/json")
        self.assertEqual(response.json(),{
            'board' : [{
                'boardId'     : 1,
                'boardName'   : 'board1',
                'pinId'       : [1],
                'pinImageUrl' : ['https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg']
            }]
        })
        self.assertEqual(response.status_code, 200)

class MypagePinTest(TestCase):
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
            email           = 'dgk089@gmail.com',
            image_url       = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            gender          = Gender.objects.get(id=1),
            region          = Region.objects.get(id=1),
            language        = Language.objects.get(id=1),
            social_platform = SocialPlatform.objects.get(id=1),
            follower_number = 12
        )
        Pin.objects.create(
            id               = 1,
            internal_account = Account.objects.get(id=1),
            external_account = Account.objects.get(id=1),
            image_url        = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            title            = 'hello',
            detail           = 'hi',
            link             = 'https://twitter.com/'
        )
    def tearDown(self):
        SocialPlatform.objects.all().delete()
        Gender.objects.all().delete()
        Region.objects.all().delete()
        Language.objects.all().delete()
        Account.objects.all().delete()
        Pin.objects.all().delete()

    def test_mypage_pin_get_success(self):
        client = Client()
        headers = {"HTTP_AUTHORIZATION" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRnazA4OUBnbWFpbC5jb20ifQ.vXF4ThqZuqYA9Wl3NKEBIdFhqJNyadO5X3pSJFIUF8Q"}
        response = client.get('/boardpin/mypagepin', **headers, content_type="application/json")
        self.assertEqual(response.json(),{
            'pin' : [{
                'pinTitle' : 'hello',
                'pinImage' : 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
                'pinLink'  : 'https://twitter.com/'
            }]
        })
        
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
        Pin.objects.create(
            id               = 1,
            internal_account = Account.objects.get(id=1),
            external_account = Account.objects.get(id=1),
            image_url        = 'https://i.pinimg.com/44/48/a7/11118e7efc90286a8dff112211dea9750.jpg',
            title            = 'hello',
            detail           = 'hi',
            link             = 'https://twitter.com/'
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
        Pin.objects.all().delete()
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