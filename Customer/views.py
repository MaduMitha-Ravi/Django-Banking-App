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
from Banker.factorydesignpattern import FactoryPattern

@login_required()
def customer_logout(request):
    logout(request)
    return render(request, 'Customer/customer_logout.html', {})#HttpResponseRedirect(reverse('login'))

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if is_user_customer(username) == 1:
            if FactoryPattern.check_status(username) == 'True':
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active: 
                        login(request, user)
                        return customermainpage(request)
                        #table = Transactions.objects.all().filter(id = User.objects.get(username=username).pk)
                        #return render(request, 'Customer/customermainpage.html', {'table': table})#HttpResponseRedirect(reverse('login'))  
                else:
                    messages.error(request, ('Invalid credentials!'))
                    return render(request, 'Customer/customer_login.html', {})
            else:
                    messages.error(request, ('Customer is Inactive!'))
                    return render(request, 'Customer/customer_login.html', {})
        else:
                messages.error(request, ('User does not exist!'))
                return render(request, 'Customer/customer_login.html', {})
            
    return render(request, 'Customer/customer_login.html', {}) #HttpResponse("Invalid login details given")



def is_user_customer(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" WHERE username = %s", [username])
        #print(cursor.rowcount)
        rowcount = cursor.rowcount 
        connection.close()
        return rowcount

@login_required()
def stocktrading(request):
    
    #form = StockWatchlistForm(request.POST)
    table = StockWatchlist.objects.all().filter(id = User.objects.get(username=request.user.username).pk)

    context = {'table': table}
    if request.POST:
        stock_symbol = request.POST.get('stock_symbol')
        #print(request.POST.get('stock_symbol1'))
        #print(request.POST)
        if 'addstock' in request.POST:
            stock_symbol = request.POST.get('stock_symbol1')
            #print(request.POST.get('stock_symbol1'))
            if validate_stockwatchlist(request, stock_symbol) == 1:
                add_stock(request, stock_symbol)
            context = {'table': table}
        elif 'removestock' in request.POST:
            stock_symbol = request.POST.get('stock_symbol1')
            if validate_stockwatchlist(request, stock_symbol) == 0:
                remove_stock(request, stock_symbol)
            context = {'table': table}
        elif 'buystock' in request.POST:
            stock_buy_sell(request)
            context = {'table': table}
            #buy_stock(request, stocktrade_pk, stock_symbol, stock_count, stock_price)
        elif 'sellstock' in request.POST:
            stock_buy_sell(request)
            context = {'table': table}
            #sell_stock(request, stocktrade_pk, stock_symbol, stock_count, stock_price)
        elif 'stock_dropdown' in request.POST:
            selected_stock = request.POST.get('stock_dropdown_symbol')
            print(selected_stock)
            plot1 = display_graph(request, selected_stock)
            context = {'table': table, 'plot1': plot1}

    return render(request, 'Customer/stocktrading.html', context = context)


def display_graph(request, selected_stock):
    
    tickerData = yf.Ticker(selected_stock)
    today = date.today()

    # dd/mm/YY
    todaydate = today.strftime("%Y-%m-%d")
    tickerDf = tickerData.history(period='1d', start='2020-12-1', end=todaydate)
    
    #plot1 = plot(px.line(tickerDf, x=tickerDf.index, y='Close'), output_type='div', include_plotlyjs=False)
    
    fig = admin_stats_plot = px.line(tickerDf, x=tickerDf.index, y='Close', title="Stock Trendline - Closing Daily Stats from 01/12/2020 ", )
    fig.layout.update({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    plot1 = plot(fig, output_type='div', include_plotlyjs=False)

    return plot1

def validate_stockwatchlist(request, stock_symbol):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            results = cursor.execute("SELECT stock_symbol FROM public.\"Customer_stockwatchlist\" WHERE id_id = '%d'" %(int(User.objects.get(username=request.user.username).pk)))
            user_stocks = cursor.fetchall()
            tmp = []
            for j in user_stocks:
                i = ' '.join([str(elem) for elem in j])
                i = i.replace('(', '')
                i = i.replace('\'', '')
                i = i.replace(',)', '')
                tmp.append(i)

        if stock_symbol in tmp:
            messages.error(request, ('Stock Symbol already exists in your Watchlist.'))
            return 0
        else:
            messages.error(request, ('Stock Symbol does not exist in your Watchlist.'))
            return 1
        

@login_required()
def add_stock(request, new_stock_symbol):

    if request.method == 'POST':
        id = User.objects.get(username=request.user.username).pk
        print(id)

        with connection.cursor() as cursor:
            results = cursor.execute("INSERT INTO public.\"Customer_stockwatchlist\" (stock_symbol, id_id) VALUES ('%s', '%d')" %(new_stock_symbol, int(User.objects.get(username=request.user.username).pk)))
            connection.commit()
        messages.success(request, ('Stock Symbol added to your Watchlist.'))
    
    table = StockWatchlist.objects.all().filter(id = User.objects.get(username=request.user.username).pk)

    return render(request, 'Customer/stocktrading.html', {'table': table})

@login_required()
def remove_stock(request, new_stock_symbol):
    if request.method == 'POST':
        id = User.objects.get(username=request.user.username).pk
        
        with connection.cursor() as cursor:
            results = cursor.execute("DELETE FROM public.\"Customer_stockwatchlist\" WHERE stock_symbol = '%s' and id_id = '%d'" %(new_stock_symbol, int(id)))
            connection.commit()
        messages.success(request, ('Stock Symbol removed from your Watchlist.'))
     
    table = StockWatchlist.objects.all().filter(id = User.objects.get(username=request.user.username).pk)[:10]

    return render(request, 'Customer/stocktrading.html', {'table': table})

@login_required()
def customermainpage(request):

    table = Transactions.objects.all().filter(id = User.objects.get(username=request.user.username).pk)
    table1 = LoanRequest.objects.all().filter(id = User.objects.get(username=request.user.username).pk)

    context = { 'table': table ,  'table1': table1 }

    return render(request, 'Customer/customermainpage.html', context=context)

def get_accountid(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" where username = '%s'" %request.user.username)
        account_id = cursor.fetchone()
        i = ' '.join([str(elem) for elem in account_id])
        i = i.replace('(', '')
        i = i.replace('\'', '')
        i = i.replace(',)', '')
        account_id = i

    #print(account_id)
    return account_id

@login_required()
def applyloan(request):

    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            username=request.user.username
            account_id = get_accountid(request)
            id_id = User.objects.get(username=username).pk
            #print(account_id, username)
            if get_loan_details(request) < 5:
                output = form.save(commit = False)
                output.account_id = User.objects.get(username=username).pk
                output.id_id = User.objects.get(username=username).pk
                output.save()
                #print('You are successfully signed up!')
                print(output.pk)
                messages.success(request, ('Loan Request Submitted successful! Loan request ID is %s') % output.loan_id)
                
                return render(request, 'Customer/applyloan.html', {'form': form})
            else:
                messages.error(request, ('Loan Request limit exceeded!'))
                
                return render(request, 'Customer/applyloan.html', {'form': form})
            
    else:
        form = LoanRequestForm()

    return render(request, 'Customer/applyloan.html', {'form': form})


def get_loan_details(request):

    with connection.cursor() as cursor:
        results = cursor.execute("SELECT count(loan_id) FROM public.\"Customer_loanrequest\" WHERE id_id = '%d' and loan_status = 'Decision Pending'" %(User.objects.get(username=request.user.username).pk))
        loan_count = cursor.fetchone()
        i = ' '.join([str(elem) for elem in loan_count])
        i = i.replace('(', '')
        i = i.replace('\'', '')
        i = i.replace(',)', '')
        loan_count = int(i)
        connection.close()

    return loan_count

@login_required()
def stock_buy_sell(request):

    form = StockTradeForm(request.POST)
    
    if request.POST:
        if form.is_valid():
            sel_stock_symbol = request.POST.get('stock_symbol')
            stock_count = request.POST.get('stock_count')
            stock_price = request.POST.get('stock_price')
            output = form.save(commit = False)
            
            id = request.user.pk
            
            output.id = int(id)
            #output = form.save(update_fields=['id', 'sel_stock_symbol', 'stock_count','stock_price'])
            output.save()
            print(output.pk)
            stocktrade_pk = output.pk

        messages.success(request, ('Stock Bid placed.'))
        
        if 'buystock' in request.POST:
            buy_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price)
        elif 'sellstock' in request.POST:
            sell_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price)

    return render(request, 'Customer/stocktrading.html', {'form': form})


@login_required()
def buy_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price):

    form = StockTradeForm(request.POST)

    account_id = get_accountid(request)

    if request.method == 'POST':
        id = User.objects.get(username=request.user.username).pk

        account_balance = account_balance_validation(request, id)

        amount_to_bid = int(stock_count) * int(stock_price)

        tickerdf_high, tickerdf_low = stock_actual_price(sel_stock_symbol)

        if amount_to_bid < account_balance:

            if (int(stock_price) < tickerdf_high).bool():
                if (int(stock_price) > tickerdf_low).bool():
                    with connection.cursor() as cursor:
                        results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Stock bought successfully' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                        connection.commit()
                        connection.close()

                    with connection.cursor() as cursor:
                        results = cursor.execute("INSERT INTO public.\"Customer_transactions\" (transaction_amount_currency, transaction_amount, transaction_status, transaction_message, transaction_timestamp, transaction_type, account_id_id, id_id) VALUES ('CAD', '%d', 'Posted', 'Stock Buy', CURRENT_TIMESTAMP, 'DEBIT', '%d', '%d')" %(amount_to_bid, int(account_id), int(id)))
                        connection.commit()
                        connection.close()

                    new_account_balance = account_balance - amount_to_bid
                    with connection.cursor() as cursor:
                        results = cursor.execute("UPDATE public.\"Banker_registercustomers\" SET depositamount = '%d' WHERE account_id = '%d' " %(new_account_balance, int(account_id)))     
                    connection.commit()
                    connection.close()

                    messages.success(request, ('%s Stocks bought successfully.' %sel_stock_symbol))

                    
                else:
                    with connection.cursor() as cursor:
                        results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Declined low value' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                        connection.commit()
                    messages.warning(request, ('Stock bid was low!'))
            else:
                with connection.cursor() as cursor:
                        results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Declined high value' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                        connection.commit()
                cursor.close()
                messages.warning(request, ('Stock bid was high!'))
                
        elif amount_to_bid >= account_balance:
            with connection.cursor() as cursor:
                results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Stock bid failed' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                connection.commit()
            messages.error(request, ('Low Account Balance!'))
            
    return render(request, 'Customer/stocktrading.html', {'form': form})

@login_required()
def sell_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price):
    form = StockTradeForm(request.POST)

    account_id = get_accountid(request)

    if request.method == 'POST':
        id = User.objects.get(username=request.user.username).pk

        account_balance = account_balance_validation(request, id)

        amount_to_bid = int(stock_count) * int(stock_price)

        existing_stock_count = check_stock_stats(request, sel_stock_symbol)
        
        if existing_stock_count != 0:
            if existing_stock_count >= int(stock_count):
                with connection.cursor() as cursor:
                    results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Stock Sold successfully' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                    connection.commit()
                messages.success(request, ('%s Stocks sold successfully.' %sel_stock_symbol))


                with connection.cursor() as cursor:
                        results = cursor.execute("INSERT INTO public.\"Customer_transactions\" (transaction_amount_currency, transaction_amount, transaction_status, transaction_message, transaction_timestamp, transaction_type, account_id_id, id_id) VALUES ('CAD', '%d', 'Posted', 'Stock Sell', CURRENT_TIMESTAMP, 'CREDIT', '%d', '%d')" %(amount_to_bid, int(account_id), int(id)))
                        connection.commit()
                        connection.close()

                new_account_balance = account_balance + amount_to_bid
                
                with connection.cursor() as cursor:
                    results = cursor.execute("UPDATE public.\"Banker_registercustomers\" SET depositamount = '%d' WHERE account_id = '%d' " %(new_account_balance, int(account_id)))     
                connection.commit()
                connection.close()

            else:
                
                with connection.cursor() as cursor:
                    results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Stock bid failed' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                    connection.commit()
                messages.error(request, ('%s has Insufficient stock quatity.' %sel_stock_symbol))
        else:

            with connection.cursor() as cursor:
                results = cursor.execute("UPDATE public.\"Customer_stocktrade\" SET stock_message = 'Stock bid failed' where stocktrade_id = '%d' and stock_symbol = '%s'" %(int(stocktrade_pk),sel_stock_symbol))
                connection.commit()
            messages.warning(request, ('%s needs to be bought before selling.' %sel_stock_symbol))
            
    return render(request, 'Customer/stocktrading.html', {'form': form})

def check_stock_stats(request, sel_stock_symbol):
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(stock_count) FROM public.\"Customer_stocktrade\" where stock_symbol = '%s' and stock_message = 'Stock bought successfully' and id = '%d' " %(sel_stock_symbol, int(User.objects.get(username=request.user.username).pk)))
        existing_buy_stock_count = cursor.fetchone()
        i = ' '.join([str(elem) for elem in existing_buy_stock_count])
        i = i.replace('(', '')
        i = i.replace('\'', '')
        i = i.replace(',)', '')
        if i == 'None':
            existing_buy_stock_count = 0
        else:
            existing_buy_stock_count = int(float(i))
        

    with connection.cursor() as cursor1:
        cursor1.execute("SELECT sum(stock_count) FROM public.\"Customer_stocktrade\" where stock_symbol = '%s' and stock_message = 'Stocks sold successfully.' and id = '%d' " %(sel_stock_symbol, int(User.objects.get(username=request.user.username).pk)))
        existing_sell_stock_count = cursor1.fetchone()


        i = ' '.join([str(elem) for elem in existing_sell_stock_count])
        i = i.replace('(', '')
        i = i.replace('\'', '')
        i = i.replace(',)', '')
        if i == 'None':
            existing_sell_stock_count = 0
        else:
            existing_sell_stock_count = int(float(i))

        existing_stock_count = existing_buy_stock_count - existing_sell_stock_count
        print(existing_stock_count)

    return existing_stock_count

def account_balance_validation(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT depositamount FROM public.\"Banker_registercustomers\" where username = '%s'" %request.user.username)
        balance = cursor.fetchone()
        i = ' '.join([str(elem) for elem in balance])
        i = i.replace('(', '')
        i = i.replace('\'', '')
        i = i.replace(',)', '')
        balance = int(float(i))

    return balance


def stock_actual_price(stock_symbol):
    tickerData = yf.Ticker(stock_symbol)
    today = date.today()
    todaydate = today.strftime("%Y-%m-%d")
    #tickerDf = tickerData.history(period='1d', start='2020-12-1', end=todaydate)
    tickerDf = tickerData.history(period='1d', start=todaydate, end=todaydate)
    print(tickerDf['High'], tickerDf['Low'])

    return tickerDf['High'], tickerDf['Low']

