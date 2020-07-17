from django.urls    import (
    path,
    include
)

urlpatterns = [
    path('boardpin', include('board_pin.urls')),
    path('account', include("account.urls"))
]
