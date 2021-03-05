from django.shortcuts import render
from django import forms
from Customer.forms import UserForm, LoanRequestForm, TransactionsForm, StockWatchlistForm, StockTradeForm
from Customer.models import Transactions, StockWatchlist, StockTrade, LoanRequest
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
from Customer.View.customervalidation import CustomerValidation

class StockWatchlistActivities:

	@login_required()
	def display_graph(request, selected_stock):
		
		tickerData = yf.Ticker(selected_stock)
		today = date.today()
		todaydate = today.strftime("%Y-%m-%d")
		tickerDf = tickerData.history(period='1d', start='2020-12-1', end=todaydate)
		
		fig = admin_stats_plot = px.line(tickerDf, x=tickerDf.index, y='Close', title="Stock Trendline - Closing Daily Stats from 01/12/2020 ", )
		fig.layout.update({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
		plot1 = plot(fig, output_type='div', include_plotlyjs=False)

		return plot1

	
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
			