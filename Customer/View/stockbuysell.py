from Customer.View.customervalidation import CustomerValidation
from django.shortcuts import render
from django import forms
from Customer.forms import UserForm, LoanRequestForm, TransactionsForm, StockWatchlistForm, StockTradeForm
from Customer.models import Transactions, StockWatchlist, StockTrade, LoanRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from django.template import Context
#from datetime import date
from datetime import date, timedelta
import yfinance as yf
from Customer.View.customervalidation import CustomerValidation
from Customer.View.stockwatchlist import StockWatchlistActivities

class StockBuySell:


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
				
				output.save()
				print(output.pk)
				stocktrade_pk = output.pk

			messages.success(request, ('Stock Bid placed.'))
			
			if 'buystock' in request.POST:
				StockBuySell.buy_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price)
			elif 'sellstock' in request.POST:
				StockBuySell.sell_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price)

		return render(request, 'Customer/stocktrading.html', {'form': form})


	@login_required()
	def buy_stock(request, stocktrade_pk, sel_stock_symbol, stock_count, stock_price):

		form = StockTradeForm(request.POST)

		account_id = CustomerValidation.get_accountid(request)

		if request.method == 'POST':
			id = User.objects.get(username=request.user.username).pk

			account_balance = CustomerValidation.account_balance_validation(request, id)

			amount_to_bid = int(stock_count) * int(stock_price)

			tickerdf_high, tickerdf_low = StockBuySell.stock_actual_price(sel_stock_symbol)

			if (int(amount_to_bid) < int(account_balance)).bool():

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

		account_id = CustomerValidation.get_accountid(request)

		if request.method == 'POST':
			id = User.objects.get(username=request.user.username).pk

			account_balance = CustomerValidation.account_balance_validation(request, id)

			amount_to_bid = int(stock_count) * int(stock_price)

			existing_stock_count = StockBuySell.check_stock_stats(request, sel_stock_symbol)
			
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

	@login_required()
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

	
	def stock_actual_price(stock_symbol):
		tickerData = yf.Ticker(stock_symbol)
		today = date.today()
		if today.isoweekday() == 6:
			yesterday = (today - timedelta(days = 2)).strftime("%Y-%m-%d")
			todaydate = (today - timedelta(days = 1)).strftime("%Y-%m-%d")
		elif today.isoweekday() == 7:
			yesterday = (today - timedelta(days = 3)).strftime("%Y-%m-%d")
			todaydate = (today - timedelta(days = 2)).strftime("%Y-%m-%d")
		else:
			yesterday = today - timedelta(days = 1)
			todaydate = today.strftime("%Y-%m-%d")
		tickerDf = tickerData.history(period='1d', start=yesterday, end=todaydate)
		print('Stocks:')
		print(tickerDf['High'])
		print(tickerDf['Low'])

		return tickerDf['High'], tickerDf['Low']
