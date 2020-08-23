from django.urls import path, include
from account import urls

urlpatterns = [
    path("account", include("account.urls")),
    path("board_pin", include("board_pin.urls")),
]
