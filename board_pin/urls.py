from django.urls import path, include

from board_pin.views import (
    CreateBoardView,
    PinDetailView,
    MypageAccountView,
    PinCreateView,
    PinListView,
)

urlpatterns = [
    path("/create-board", CreateBoardView.as_view()),
    path("/pin", PinDetailView.as_view()),
    path("/mypageaccount", MypageAccountView.as_view()),
    path("/pincreate", PinCreateView.as_view()),
    path("/homepin", PinListView.as_view()),
]