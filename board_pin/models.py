from django.db import models

class Pin(models.Model):
    image_url        = models.URLField(max_length=300)
    title            = models.CharField(max_length=5000, null=True)
    detail           = models.CharField(max_length=5000, null=True)
    link             = models.CharField(max_length=5000, null=True)
    interest         = models.ForeignKey('account.Interest', on_delete=models.SET_NULL, null=True)
    internal_account = models.ForeignKey('account.Account', on_delete=models.CASCADE, null=True, related_name='internal_account')
    external_account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, null=True, related_name='external_account')
    comment          = models.ForeignKey('account.Comment', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'pins'

class Board(models.Model):
    name       = models.CharField(max_length=5000)
    start_date = models.DateField(null=True)
    end_date   = models.DateField(null=True)
    secret     = models.BooleanField(null=True)
    account    = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    pin        = models.ManyToManyField('Pin', through='BoardPin')
    
    class Meta:
        db_table = 'boards'

class BoardPin(models.Model):
    board = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True)
    pin   = models.ForeignKey('Pin', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'board_pins'

class AccountBoardPin(models.Model):
    account   = models.ForeignKey('account.Account', on_delete=models.CASCADE, null=True)
    board_pin = models.ForeignKey('BoardPin', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'account_board_pins'
