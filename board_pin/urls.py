from django.urls import path
from .views import CreateBoardView

urlpatterns = [
    path('/create-board', CreateBoardView.as_view())
]


