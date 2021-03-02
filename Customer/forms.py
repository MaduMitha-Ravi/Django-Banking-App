from django import forms
#from Customer.models import UserProfileInfo
from django.contrib.auth.models import User
from django.forms import HiddenInput
from Customer.models import LoanRequest, Transactions, StockWatchlist, StockTrade



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')
  
class LoanRequestForm(forms.ModelForm):
    class Meta:
        model= LoanRequest
        fields= ["loan_id",  "gender", "own_a_car", "own_a_realty", "income_type", "education_type", "family_status", "housing_type", "occupation_type", "loan_amount", "income_amount"]       
        labels = {
        "gender" : ('Select your Gender'), "own_a_car" : ('Do you own a Car?'), "own_a_realty" : ('Do you own a Realty?'), "income_type" : ('Select your Income Type'), "education_type" : ("Select your education level"), "family_status" : ('Select your Marital Status'), "housing_type" : ('Select your Housing Type'),"occupation_type" : ('Select your Occupation Type'), "loan_amount" : ('Enter Loan Amount'), "income_amount": ('Enter Annual Income'),
        }
        widgets = {'loan_status': forms.HiddenInput(),'account_id': forms.HiddenInput(), 'id': forms.HiddenInput() }


class TransactionsForm(forms.ModelForm):
    class Meta:
        model= Transactions
        fields= ["transaction_amount",  "transaction_message", "transaction_type"]       
        labels = {
        "transaction_amount" : ('Enter Transaction Amount'), "transaction_message" : ('Enter reason for Transaction'), "transaction_type" : ('Select Transaction Type')
        }
        widgets = {'transactionreferencenumber': forms.HiddenInput(),'account_id': forms.HiddenInput(),
        'transaction_status': forms.HiddenInput(),'transaction_timestamp': forms.HiddenInput(), 'id': forms.HiddenInput(), }

class StockWatchlistForm(forms.ModelForm):
    class Meta:
        model = StockWatchlist
        fields = ["stock_symbol"]
        labels = {"stock_symbol": ('Enter Stock Symbol')}
        widgets = {'stockwatchlist_id': forms.HiddenInput(),'id': forms.HiddenInput(),}


class StockTradeForm(forms.ModelForm):
    class Meta:
        model = StockTrade
        fields = ["stock_symbol", "stock_count", "stock_price"]
        labels = {"stock_symbol": ('Enter Stock Symbol'), "stock_count": ('Enter Stock count'), "stock_price": ('Enter Stock bidding price')}
        widgets = {'stocktrade_id': forms.HiddenInput(),'id': forms.HiddenInput(), 'stock_message': forms.HiddenInput(),}


