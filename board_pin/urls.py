from django.urls import path
from .views import (
    CreateBoardView,
    PinCreateView
)

urlpatterns = [
    path('/create-board', CreateBoardView.as_view()),
    path('/pincreate', PinCreateView.as_view())
]