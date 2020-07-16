import json
import boto3

from django.views import View
from django.http  import (
    JsonResponse,
    HttpResponse
)

from board_pin.models import (
    Pin,
    Board,
    BoardPin
)

from account.models import Account
from account.utils  import decorator_login

from datetime import datetime

from dkinterest.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)

class PinCreateView(View):
    @decorator_login
    def post(self, request):
        user_id = request.user.id
        
        # image
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )

        image = request.FILES['filename']
        image_time = (str(datetime.now())).replace(" ","")
        image_type = (image.content_type).split("/")[1]
        s3_client.upload_fileobj(
            image,
            "dkinterest",
            image_time+"."+image_type,
            ExtraArgs = {
                "ContentType" : image.content_type
            }
        )
        image_url = "http://dkinterest.s3.ap-northeast-2.amazonaws.com/"+image_time+"."+image_type
        image_url = image_url.replace(" ","/")

        # pin
        pin = Pin.objects.create(
            internal_account_id = user_id,
            image_url           = image_url,
            title               = request.POST.get('title'),
            detail              = request.POST.get('detail'),
            link                = request.POST.get('link'),
            interest_id         = 1
        )
        return HttpResponse(status=200)