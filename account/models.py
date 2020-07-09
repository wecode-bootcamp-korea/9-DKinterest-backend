from django.db import models
from board_pin.models import (
    Pin,
    Board,
    BoardPin,
    AccountBoardPin
)

class Account(models.Model):
    email             = models.EmailField(max_length=100, null=True, unique=True)
    password          = models.CharField(max_length=500, null=True)
    nickname          = models.CharField(max_length=100, unique=True)
    age               = models.IntegerField(null=True)
    name              = models.CharField(max_length=50)
    follower_number   = models.IntegerField(default=0)
    image_url         = models.URLField(max_length=300, null=True)
    gender            = models.ForeignKey('Gender', on_delete=models.CASCADE)
    region            = models.ForeignKey('Region', on_delete=models.CASCADE)
    language          = models.ForeignKey('Language', on_delete=models.CASCADE)
    social_platform   = models.ForeignKey('SocialPlatform', on_delete=models.CASCADE)
    interest          = models.ManyToManyField('Interest', through='AccountInterest',related_name='interest')
    board_pin         = models.ManyToManyField('board_pin.BoardPin', through='board_pin.AccountBoardPin', related_name='board_pin')
    comment           = models.ManyToManyField('Comment', through='AccountCommentLike', related_name='+')

    class Meta:
        db_table = 'accounts'

class SocialPlatform(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'social_platforms'

class Gender(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'genders'

class Region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'regions'

class Language(models.Model):
    language = models.CharField(max_length=100)

    class Meta:
        db_table = 'languages'

class Interest(models.Model):
    title     = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)

    class Meta:
        db_table = 'interests'

class AccountInterest(models.Model):
    account  = models.ForeignKey('Account', on_delete=models.CASCADE)
    interest = models.ForeignKey('Interest', on_delete=models.CASCADE)

    class Meta:
        db_table = 'account_interests'

class Following(models.Model):
    from_following = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, related_name='from_following')
    to_following   = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, related_name='to_following')
    
    class Meta:
        db_table = 'followings'

class Comment(models.Model):
    account        = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='account_comment')
    content        = models.CharField(max_length=1000)
    mother_comment = models.ForeignKey('self', max_length=1000, on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        db_table = 'comments'

class AccountCommentLike(models.Model):
    is_like = models.BooleanField(default=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'account_comment_likes'
