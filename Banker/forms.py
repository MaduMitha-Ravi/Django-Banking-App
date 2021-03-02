from django import forms
#from Banker.models import UserProfileInfo
from django.contrib.auth.models import User
from Banker.models import RegisterCustomers

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')
        
class RegisterCustomerForm(forms.ModelForm):
    class Meta:
        model= RegisterCustomers
        fields= ["account_id", "firstname", "lastname", "sin", "email", "zipcode", "contactnumber", "accounttype", "depositamount", "username", "password"]       
        labels = {
        "firstname" : ('Enter First Name'), "lastname" : ('Enter Last Name'), "sin" : ('Enter SIN'), "email" : ('Enter valid Email ID'), "zipcode" : ('Enter Zipcode'), "contactnumber" : ('Enter Contact Number'), "accounttype" : ('Select Account Type'),"depositamount" : ('Enter Amount to Deposit in account'), "username" : ('Enter UserName for your profile'), "password" : ('Enter Password'),
        }

