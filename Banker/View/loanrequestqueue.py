from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from Customer.forms import LoanRequestForm
from Customer.models import LoanRequest
from django.db import connection

from Customer.views import Customer
from Banker.View.observerdesignpattern_loanstatus import ObserverPattern
from Banker.View.machinelearning import machinelearning

from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import pandas as pd


class loanrequestqueue:

	@login_required(login_url='/Banker/banker_login/')
	def loan_status_update_approve(request):
	    if request.method == 'POST':
	        loan_id_selected = request.POST.get('approve_loan')
	        if len(loan_id_selected) != 0: 
	            with connection.cursor() as cursor:
	                results = cursor.execute("UPDATE public.\"Customer_loanrequest\" SET loan_status = 'Approved' where loan_id = %s" %loan_id_selected)
	            messages.success(request, ('Loan Request Approved.'))
	            loan_message = 'Approved'
	            ObserverPattern(request, loan_message)
	           
	    return render(request, 'Banker/loanrequest.html', {})


	@login_required(login_url='/Banker/banker_login/')
	def loan_status_update_decline(request):
	    if request.method == 'POST':
	        loan_id_selected = request.POST.get('decline_loan')
	        if len(loan_id_selected) != 0: 
	            with connection.cursor() as cursor:
	                results = cursor.execute("UPDATE public.\"Customer_loanrequest\" SET loan_status = 'Declined' where loan_id = %s" %loan_id_selected)
	            messages.error(request, ('Loan Request Declined.'))
	            loan_message = 'Declined'
	            ObserverPattern(request, loan_message)

	    return render(request, 'Banker/loanrequest.html', {})

	@login_required(login_url='/Banker/banker_login/')
	def loan_prediction(request):
	    if request.method == 'POST':
	        loan_id_selected = request.POST.get('loan_prediction')
	        with connection.cursor() as cursor:
	            cursor.execute("SELECT gender, own_a_car, own_a_realty,  loan_amount, income_type, education_type, family_status, housing_type, occupation_type FROM public.\"Customer_loanrequest\" where loan_id = %s" %loan_id_selected)
	            results = cursor.fetchone()
	            
	        print(results)
	        model = machinelearning.machinelearning()
	        
	        prediction = model.predict([results]) # model.predict([results])
	        print(prediction[0])

	        if prediction[0] == 0 :
	            messages.info(request, ('Prediction: Loan can be approved with 82 percent accuracy! '))
	        if prediction[0] == 1 :
	            messages.info(request, ('Prediction: Loan can be declined with 82 percent accuracy!'))
	      
	    return render(request, 'Banker/loanrequest.html', {})

