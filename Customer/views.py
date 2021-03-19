from django.shortcuts import render
from django import forms
from Customer.forms import UserForm, LoanRequestForm, TransactionsForm, StockWatchlistForm, StockTradeForm
from Customer.models import Transactions, StockWatchlist, StockTrade, LoanRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from django.template import Context
from datetime import date
import plotly.express as px
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.shortcuts import render
import numpy as np
from Banker.View.factorydesignpattern_bankeradmin import FactoryPattern
from Customer.View.customervalidation import CustomerValidation
from Customer.View.stockwatchlist import StockWatchlistActivities
from Customer.View.stockbuysell import StockBuySell
from Customer.View.loanapplication import LoanApplication

class Customer:

    @login_required()
    def customer_logout(request):
        logout(request)
        return render(request, 'Customer/customer_logout.html', {})

    def customer_login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if CustomerValidation.is_user_customer(username) == 1:
                if FactoryPattern.check_status(username) == 'True':
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active: 
                            login(request, user)
                            return HttpResponseRedirect('/Customer/customermainpage/')
                                    
                    else:
                        messages.error(request, ('Invalid credentials!'))
                        return render(request, 'Customer/customer_login.html', {})
                else:
                        messages.error(request, ('Customer is Inactive!'))
                        return render(request, 'Customer/customer_login.html', {})
            else:
                    messages.error(request, ('User does not exist!'))
                    return render(request, 'Customer/customer_login.html', {})
                
        return render(request, 'Customer/customer_login.html', {}) 

    @login_required()
    def stocktrading(request):
        
        table = StockWatchlist.objects.all().filter(id = User.objects.get(username=request.user.username).pk)

        context = {'table': table}
        if request.POST:
            stock_symbol = request.POST.get('stock_symbol')
            
            if 'addstock' in request.POST:
                stock_symbol = request.POST.get('stock_symbol1')
                
                if CustomerValidation.validate_stockwatchlist(request, stock_symbol) == 1:
                    StockWatchlistActivities.add_stock(request, stock_symbol)
                context = {'table': table}
            elif 'removestock' in request.POST:
                stock_symbol = request.POST.get('stock_symbol1')
                if CustomerValidation.validate_stockwatchlist(request, stock_symbol) == 0:
                    StockWatchlistActivities.remove_stock(request, stock_symbol)
                context = {'table': table}
            elif 'buystock' in request.POST:
                StockBuySell.stock_buy_sell(request)
                context = {'table': table}
                
            elif 'sellstock' in request.POST:
                StockBuySell.stock_buy_sell(request)
                context = {'table': table}
                
            elif 'stock_dropdown' in request.POST:
                selected_stock = request.POST.get('stock_dropdown_symbol')
                
                plot1 = StockWatchlistActivities.display_graph(request, selected_stock)
                context = {'table': table, 'plot1': plot1}

        return render(request, 'Customer/stocktrading.html', context = context)

    @login_required()
    def customermainpage(request):

        table = Transactions.objects.all().filter(id = User.objects.get(username=request.user.username).pk).order_by('-transaction_timestamp')[:6]
        table1 = LoanRequest.objects.all().filter(id = User.objects.get(username=request.user.username).pk).order_by('-loan_id')[:2]

        context = { 'table': table ,  'table1': table1 }
        
        loan_status = CustomerValidation.get_loan_latest_status(request)
	#messages.INFO(request, ' %s ' % loan_status)
	#print(loan_status)
        messages.light(request, ('%s') % loan_status)
					
        return render(request, 'Customer/customermainpage.html', context=context)    

    @login_required()
    def applyloan(request):

        if request.method == 'POST':
            
            return LoanApplication.loanapplicationform(request)
                
        else:
            form = LoanRequestForm()

            return render(request, 'Customer/applyloan.html', {'form': form})


    

    


    

