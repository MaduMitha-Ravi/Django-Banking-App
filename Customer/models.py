from django.db import models
from django.contrib.auth.models import User
from django import forms
from djmoney.models.fields import MoneyField
from phone_field import PhoneField
from Banker.models import RegisterCustomers


gender_choices = (('1','Male'), ('0', 'Female'))
car_choices = (('0','Yes'), ('1', 'No'))
realty_choices = (('0','Yes'), ('1', 'No'))
income_type_choices = (('0', 'Working'),  ('1', 'Student'), ('2' , 'Not Working'))
education_type_choice = (('1', 'Graduate'), ('0' , 'Not Graduated'))
family_status_choices = (('1' , 'Married'), ('0' , 'Not Married'))
housing_type_choices = (('1' , 'Home/Apartment'), ('0', 'Others'))
occupation_type_choices = (('0', 'IT/Medical/Manager/Secretaries'), ('1', 'Staffs'), ('2', 'Others'))
# Create your models here.

class LoanRequest(models.Model):

    loan_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    gender = models.CharField( max_length=20, choices=gender_choices, default = '' ) 
    own_a_car = models.CharField(max_length=20, choices=car_choices, default = '' ) 
    own_a_realty = models.CharField(max_length=20,  choices=realty_choices, default = '' ) 
    income_type = models.CharField(max_length=20,  choices=income_type_choices, default = '' ) 
    education_type = models.CharField(max_length=20,  choices=education_type_choice, default = '' ) 
    family_status = models.CharField( max_length=20, choices=family_status_choices, default = '' )
    housing_type = models.CharField( max_length=20, choices=housing_type_choices, default = '' ) 
    occupation_type = models.CharField( max_length=40, choices=occupation_type_choices, default = '' )
    income_amount = models.IntegerField() #MoneyField(max_digits=20, decimal_places=2, default_currency='CAD')
    loan_amount = MoneyField(max_digits=20, decimal_places=2, default_currency='CAD')
    loan_status = models.CharField(max_length=30, default = 'Decision Pending')
    id = models.ForeignKey(User, on_delete=models.CASCADE)

transaction_type_choices = (('Credit', 'Credit'), ('Debit', 'Debit'))

class Transactions(models.Model):
    transactionreferencenumber = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(RegisterCustomers, on_delete=models.CASCADE)
    transaction_amount = MoneyField(max_digits=20, decimal_places=2, default_currency='CAD')
    transaction_status = models.CharField( max_length=20)
    transaction_message = models.CharField( max_length=20)
    transaction_timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField( max_length=20, choices=transaction_type_choices, default = '')
    id = models.ForeignKey(User, on_delete=models.CASCADE)


class StockWatchlist(models.Model):
    stockwatchlist_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField( max_length=20)


class StockTrade(models.Model):
    stocktrade_id = models.AutoField(primary_key=True)
    id = models.IntegerField()#ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField( max_length=20)
    stock_count = models.IntegerField()
    stock_price = models.IntegerField()
    stock_message = models.CharField( max_length=50, default = 'Initiated')


def __str__(self):
    return self.user.username   