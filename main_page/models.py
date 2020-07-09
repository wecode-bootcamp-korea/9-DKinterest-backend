from django.db import models

class MainPageInterest(models.Model):
    name = models.CharField(max_length=100)
   
    class Meta:
        db_table = 'main_page_interests'

class MainPage(models.Model):
    image_url          = models.URLField(max_length=300)
    main_page_interest = models.ForeignKey('MainPageInterest', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'main_pages'
