from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class userProfile(models.Model):
    userFK = models.ForeignKey(User, verbose_name=("User ID"), on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False,blank=True,null=True)
    subscription_type = models.CharField(max_length=50,blank=True,null=True)
    subscription_refrence = models.CharField(max_length=100,blank=True,null=True)
    price = models.CharField(max_length=50,blank=True,null=True)
    subscription_start = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
    subscription_expiry = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
    payment_status = models.BooleanField(default=False,blank=True,null=True)
    paymentDate = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
    currency =  models.CharField(max_length=50,blank=True,null=True)
    order_ID = models.CharField(max_length=200,blank=True,null=True)
    recurring_billing = models.BooleanField(default=False,blank=True,null=True)
    agree_receive_notify = models.BooleanField(default=False,blank=True,null=True)
    agree_term_n_condition = models.BooleanField(default=False,blank=True,null=True)
    create_at =  models.DateTimeField( auto_now_add=True)
    modify_at =  models.DateTimeField(auto_now=True)



class UserUniqueToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)  # for token expiration


class AdminBannerTemplate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bannerHeadText = models.CharField(max_length=200)
    document = models.FileField(upload_to='documents/bannerImages/')
    bannerText = models.TextField()
    bannerSubText = models.TextField()
    create_at =  models.DateTimeField( auto_now_add=True)
    modify_at =  models.DateTimeField(auto_now=True)

class AdminPeopleCommentedTemplate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/commentedPeopleImages/')
    name = models.CharField(max_length=200)
    text = models.TextField()
    about = models.TextField()
    create_at =  models.DateTimeField( auto_now_add=True)
    modify_at =  models.DateTimeField(auto_now=True)

class prices(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_price = models.CharField(max_length=50,blank=False,null=False)
    yearly_price = models.CharField(max_length=50,null=False,blank=False)





