from django.urls import path

from board_pin.views import (
    CreateBoardView,
    PinDetailView,
    MypageBoardView,
    MypagePinView,
    MypageAccountView,
    PinCreateView
)

urlpatterns = [
    path('/create-board', CreateBoardView.as_view()),
    path('/pin', PinDetailView.as_view()),
    path('/mypageboard', MypageBoardView.as_view()),
    path('/mypagepin', MypagePinView.as_view()),
    path('/mypageaccount', MypageAccountView.as_view()),
    path('/pincreate', PinCreateView.as_view()),
    path("/homepin", PinListView.as_view())
]
