from django import forms
from Customer.forms import UserForm, LoanRequestForm, TransactionsForm, StockWatchlistForm, StockTradeForm
from Customer.models import Transactions, StockWatchlist, StockTrade, LoanRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from django.template import Context
from django.shortcuts import render
from Customer.View.customervalidation import CustomerValidation

class LoanApplication:

	@login_required()
	def loanapplicationform(request):

		form = LoanRequestForm(request.POST)
		if form.is_valid():
			username=request.user.username
			#account_id = CustomerValidation.get_accountid(request)
			#id_id = User.objects.get(username=username).pk
			
			if CustomerValidation.get_loan_details(request) < 2:
				output = form.save(commit = False)
				output.account_id = User.objects.get(username=username).pk
				output.id_id = User.objects.get(username=username).pk
				output.save()
				messages.success(request, ('Loan Request Submitted successful! Loan request ID is %s') % output.loan_id)
				
				return render(request, 'Customer/applyloan.html', {'form': form})
			else:
				messages.error(request, ('Loan Request limit exceeded!'))
				
				return render(request, 'Customer/applyloan.html', {'form': form})