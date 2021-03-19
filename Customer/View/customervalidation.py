from django.db import connection
from django.contrib.auth.models import User
from django.contrib import messages

class CustomerValidation:

	def is_user_customer(username):
		with connection.cursor() as cursor:
			cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" WHERE username = %s", [username])
			#print(cursor.rowcount)
			rowcount = cursor.rowcount 
			connection.close()
			return rowcount

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

	def get_loan_latest_status(request):
		with connection.cursor() as cursor:
			results = cursor.execute("SELECT loan_id, loan_status FROM public.\"Customer_loanrequest\" WHERE id_id = '%d' ORDER BY loan_id DESC" %(User.objects.get(username=request.user.username).pk))
			loan_id = cursor.fetchone()
			i = ' '.join([str(elem) for elem in loan_id])
			i = i.replace('(', '')
			i = i.replace('\'', '')
			i = i.replace(',)', '')
			loan_id = int(i)
			print(loan_id)
			connection.close()
		
		loan_status = ''	
		if 'Approved' in loan_id:
			loan_status = 'Congrats! Loan is Approved'
		elif 'Declined' in loan_id:
			loan_status = 'Sorry! Loan is Declined'
	
		return loan_status
		
	
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

	def get_accountid(request):

		with connection.cursor() as cursor:
			cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" where username = '%s'" %(User.objects.get(username=request.user.username)))
			account_id = cursor.fetchone()
			i = ' '.join([str(elem) for elem in account_id])
			i = i.replace('(', '')
			i = i.replace('\'', '')
			i = i.replace(',)', '')
			account_id = i

		return account_id


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
			elif stock_symbol not in tmp:
				#messages.error(request, ('Stock Symbol does not exist in your Watchlist.'))
				return 1
