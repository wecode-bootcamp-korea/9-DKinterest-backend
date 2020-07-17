from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import json

from account.utils import decorator_login
from .models import (
        Board,
        BoardPin
        )
from account.models import Account

class CreateBoardView(View):
    @decorator_login
    def post(self, request):
        board = json.loads(request.body)
        user_id = request.user.id
        try:
            print(user_id)
            if Board.objects.filter(name = board['name']).exists():
                return JsonResponse({"message": "BOARD_ALREADY_EXISTS"}, status=400)

            new_board = Board.objects.create(
                name = board['name'],
                account_id = user_id
            ).save()

            return JsonResponse({"message": "BOARD_SUCCESSFULLY_CREATED"}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "FAILED_TO_CREATE"}, status=405)
