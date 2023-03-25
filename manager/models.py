from django.db import models

# Create your models here.
class mainData(models.Model):
    userID = models.IntegerField(default=0,null=True)
    item_name = models.CharField(max_length = 100,default='item',null=True)
    price = models.BigIntegerField(default=0,null=True)
    quantity = models.IntegerField(default=0,null=True)
    post_price = models.IntegerField(default=0,null=True)

class historyData(models.Model):
    userID1 = models.IntegerField(default=0,null=True)
    O_price = models.BigIntegerField(default=0,null=True)
    C_price = models.BigIntegerField(default=0,null=True)
    Opost_price = models.IntegerField(default=0,null=True)
    Cpost_price = models.IntegerField(default=0,null=True)
    date = models.CharField(max_length = 100,default='date',null=True)
    Oquantity = models.IntegerField(default=0,null=True)
    Cquantity = models.IntegerField(default=0,null=True)
    item_name = models.TextField(max_length = 10000,default='item',null=True)
    Citem_name = models.TextField(max_length = 10000,default='item',null=True)
    historyFor = models.CharField(max_length = 100,default='history for',null=True)
    actionTime = models.TextField(default='actionTime',null=True)
    month = models.IntegerField(default=0,null=True)
    year = models.IntegerField(default=0,null=True)
    day = models.IntegerField(default=0,null=True)
    item_marker = models.IntegerField(default=0,null=True)

class userInfo(models.Model):
    user_name = models.TextField(max_length=1000,default='username',null=True)
    email = models.TextField(default='user@gmail.com',null=True)
    city = models.TextField(default='city',null=True)
    township = models.TextField(default='township',null=True)
    ward = models.TextField(default='ward',null=True)
    street = models.TextField(default='street',null=True)
    userId = models.IntegerField(default=0,null=True)
    userPswd = models.TextField(default='pswd',null=True)

    def __str__(self) -> str:
        return self.user_name
    
class userNote(models.Model):
    userId = models.IntegerField(default=0,null=True)
    user_Name = models.TextField(default="user_name",null=True)
    user_note = models.TextField(default="Notes",null=True)
    date = models.TextField(default="date",null=True)
    time = models.TextField(default="time",null=True)

    def __str__(self):
        return self.user_Name