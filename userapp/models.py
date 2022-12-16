from django.db import models

# Create your models here.
class UserRegisterModel(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(help_text='user_name',max_length=50)
    user_email=models.EmailField(help_text='user_email',max_length=100)
    user_password=models.CharField(help_text='user_password', max_length=50)
    user_twitterhandle=models.CharField(help_text='user_twitter_username',max_length=100)
    user_mobile=models.IntegerField(help_text='user_mobile')
    user_location=models.CharField(help_text='user_location',max_length=50,null=True)
    user_status=models.CharField(help_text='user_status',max_length=20,default='Pending')
    user_reg=models.DateField(auto_now=True)

    class Meta:
        db_table = 'User_details'


class TagNamesModel(models.Model):
    tagname=models.CharField(help_text='tagname',max_length=100)
    count=models.BigIntegerField(help_text='Number_of_searches',default=1)
    date=models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'tag_names'
