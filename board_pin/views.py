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

class PinDetailView(View):
    @decorator_login
    def get(self, request):
        pin_id = request.GET.get('pin_id', None)
        if Pin.objects.filter(id = pin_id).exists():
            pin_list = Pin.objects.prefetch_related('boardpin_set__board', 'external_account').get(id = pin_id)
            pin = [
                {
                    'internalAccount'    : pin_list.internal_account.name,
                    'internalAccountImg' : pin_list.internal_account.image_url,
                    'externalAccount'    : pin_list.external_account.name,
                    'externalAccountImg' : pin_list.external_account.image_url,
                    'imgUrl'             : pin_list.image_url,
                    'title'              : pin_list.title,
                    'detail'             : pin_list.detail,
                    'link'               : pin_list.link,
                    'boardName'          : pin_list.board_set.last().name,
                    'followNumber'       : pin_list.internal_account.follower_number
                }
            ]
            return JsonResponse({'pin':pin}, status=200)

        return JsonResponse({'message':'NO_PIN'}, status=400)

class MypageAccountView(View):
    @decorator_login
    def get(self, request):
        user_id = request.user.id
        account_info = Account.objects.get(id = user_id)
        account = {
                'accountId'     : account_info.id,
                'accountName'   : account_info.name,
                'accountImage'  : account_info.image_url,
                'accountFollow' : account_info.follower_number,
            }
        return JsonResponse({'account':account}, status=200)

class MypageBoardView(View):
    @decorator_login
    def get(self, request):
        user_id = request.user.id
        account_info = Account.objects.prefetch_related('board_set__pin').get(id = user_id)
        board = [
            {
                'boardId'     : board.id,
                'boardName'   : board.name,
                'pinId'       : [pin_element.pin.id for pin_element in board.boardpin_set.all()],
                'pinImageUrl' : [pin_element.pin.image_url for pin_element in board.boardpin_set.all()]
            } for board in account_info.board_set.all() ]
        return JsonResponse({'board':board}, status=200)

class MypagePinView(View):
    @decorator_login
    def get(self, request):
        user_id = request.user.id
        account_pin = Account.objects.prefetch_related('uploader_pin').get(id = user_id)
        pin = [
            {
                'pinTitle' : account.title,
                'pinImage' : account.image_url,
                'pinLink'  : account.link
            } for account in account_pin.uploader_pin.all() ]
        return JsonResponse({'pin':pin}, status=200)

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
