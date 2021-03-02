from django.db import models
from django.contrib.auth.models import User
from django import forms
from djmoney.models.fields import MoneyField
from phone_field import PhoneField

accounttype_choices = (('Savings','Savings'), ('Checkings', 'Checkings'))

# Create your models here.

class RegisterCustomers(models.Model):
    account_id = models.AutoField(primary_key=True)
    #customer_id = models.AutoField(blank=True, primary_key=False)
    firstname= models.CharField( max_length=100)
    lastname= models.CharField( max_length=100)
    sin= models.IntegerField()
    email= models.EmailField()
    zipcode= models.CharField(max_length=10)
    contactnumber= PhoneField()
    accounttype= models.CharField(max_length=20, choices=accounttype_choices, default = 'Checkings' ) 
    depositamount= MoneyField(max_digits=14, decimal_places=2, default_currency='CAD')
    username= models.CharField(max_length=30)
    password= models.CharField(max_length=20)    
   
    
def __str__(self):
    return self.user.username   