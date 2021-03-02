from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Banker.forms import RegisterCustomerForm
from Banker.models import RegisterCustomers
from django.contrib import messages
from django.contrib.auth import get_user_model
from Customer.forms import LoanRequestForm
from Customer.models import LoanRequest
from django.db import connection

from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

import pandas as pd
import numpy as np
from plotly.graph_objs import *
import plotly.express as px
from plotly.offline import plot

from twilio.rest import Client
import keyboard
from django.core.mail import send_mail
from django.conf import settings

from Customer.views import customermainpage
from Banker.observerdesignpattern import ObserverPattern
from Banker.factorydesignpattern import FactoryPattern

form = RegisterCustomerForm()


final_df = pd.read_csv('Banker/datasets/final_df.csv')
y1 = final_df['Loan_Status']
X1 = final_df.drop(['Loan_Status'], axis = 1)
X_balance,Y_balance = SMOTE().fit_sample(X1,y1)
X_train, X_test, y_train, y_test = train_test_split(X_balance,Y_balance, 
                                                    stratify=Y_balance, test_size=0.25,
                                                    random_state = 10086)

model = RandomForestClassifier(max_depth = 20)
model.fit(X_train, y_train)


@login_required(login_url='/Banker/banker_login/')
def banker_logout(request):
    logout(request)
    return render(request, 'Banker/banker_logout.html', {})#HttpResponseRedirect(reverse('login'))

def banker_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if is_user_admin(username) == 'True':
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'Banker/registercustomer.html', {'form': form})#HttpResponseRedirect(reverse('login'))  
            else:
                messages.error(request, ('Incorrect credentials!'))
                return render(request, 'Banker/banker_login.html', {})
        elif is_user_admin(username) == '':
            messages.error(request, ('User does not exist!'))
    return render(request, 'Banker/banker_login.html', {}) #HttpResponse("Invalid login details given")

def is_user_admin(username):
    user_status = ''
    with connection.cursor() as cursor:
        cursor.execute("SELECT is_superuser FROM public.auth_user WHERE username = '%s'" %username)
        rowcount = cursor.rowcount
        if rowcount != 0:
            user_status = cursor.fetchone()
            i = ' '.join([str(elem) for elem in user_status])
            i = i.replace('(', '')
            i = i.replace(',)', '')
            user_status = i
            print(user_status)
    return user_status

def is_user_customer(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" WHERE username = %s", [username])
        rowcount = cursor.rowcount
        connection.close()
        return rowcount

@login_required(login_url='/Banker/banker_login/')
def registercustomer(request):
    
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            UserModel = get_user_model()
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')

            user = UserModel.objects.create_user(username=username, password = password, first_name=first_name, last_name=last_name, email = email)
            user.save()
            output = form.save()
            #print('You are successfully signed up!')
            print(output.pk)
            messages.success(request, ('Customer Registration successful! Customer ID is %s') % output.account_id)

                #users = RegisterCustomer.objects.all()
                #return render(request, 'Banker/registercustomer.html', {'users': users})
            
            return render(request, 'Banker/registercustomer.html', {'form': form})
            
    else:
        form = RegisterCustomerForm()
    
    return render(request, 'Banker/registercustomer.html', {'form': form})

@login_required(login_url='/Banker/banker_login/')
def loanrequest(request):
    #results = valid_loan_requests()
    if request.POST:
        if 'approve_loan' in request.POST:
            loan_status_update_approve(request)
        elif 'decline_loan' in request.POST:
            loan_status_update_decline(request)
        elif 'loan_prediction' in request.POST:
            loan_prediction(request)
    
    table = LoanRequest.objects.all().filter(loan_status = 'Decision Pending')
        
    return render(request, 'Banker/loanrequest.html', {'table': table})


@login_required(login_url='/Banker/banker_login/')
def loan_status_update_approve(request):
    if request.method == 'POST':
        loan_id_selected = request.POST.get('approve_loan')
        #print(loan_id_selected)
        if len(loan_id_selected) != 0: 
            with connection.cursor() as cursor:
                results = cursor.execute("UPDATE public.\"Customer_loanrequest\" SET loan_status = 'Approved' where loan_id = %s" %loan_id_selected)
            messages.success(request, ('Loan Request Approved.'))
            loan_message = 'Approved'
            op = ObserverPattern(request, loan_message)
           # banker_loan_decision(loan_id_selected)
    return render(request, 'Banker/loanrequest.html', {})


@login_required(login_url='/Banker/banker_login/')
def loan_status_update_decline(request):
    if request.method == 'POST':
        loan_id_selected = request.POST.get('decline_loan')
        #print(len(loan_id_selected))
        if len(loan_id_selected) != 0: 
            with connection.cursor() as cursor:
                results = cursor.execute("UPDATE public.\"Customer_loanrequest\" SET loan_status = 'Declined' where loan_id = %s" %loan_id_selected)
            messages.success(request, ('Loan Request Declined.'))
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

        prediction = y_predict = model.predict([results]) 

        print(prediction[0])

        if prediction[0] == 0 :
            messages.success(request, ('Prediction: Approved!'))
        if prediction[0] == 1 :
            messages.warning(request, ('Prediction: Declined!'))
      
    return render(request, 'Banker/loanrequest.html', {})


@login_required(login_url='/Banker/banker_login/')
def customeradmin(request):
    admin_stats_plot = admin_stats(request)
    context = {'admin_stats_plot': admin_stats_plot}

    if request.POST:
        
        username = request.POST.get('username')
        if validate_username(request, username) == 0:
            if request.POST.get('dropdown') == 'disablecustomer':
                FactoryPattern.disablecustomer(request, username)
            elif request.POST.get('dropdown') == 'deletecustomer': 
                FactoryPattern.deletecustomer(request, username)
            elif request.POST.get('dropdown') == 'enablecustomer': 
                FactoryPattern.enablecustomer(request, username)

    admin_stats_plot = admin_stats(request)
    context = {'admin_stats_plot': admin_stats_plot}

    return render(request, 'Banker/customeradmin.html', context = context)

def validate_username(request, username):
    if len(username) != 0: 
        if is_user_customer(username) == 0:
            messages.warning(request, ('Please enter valid username!'))
        else:
            return 0
    elif len(username) == 0: 
        messages.warning(request, ('Please enter username before proceeding!'))


def admin_stats(request):
    
    category = ['Active Customers', 'Inactive Customers']
    category_counts = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT count(is_active) FROM public.auth_user group by is_active")
        category_count = cursor.fetchall()

        for i in category_count:
            i = ' '.join([str(elem) for elem in i])
            i = i.replace('(', '')
            i = i.replace(',)', '')
            category_counts.append(int(i))

    #admin_stats_plot = plot(px.pie(values=category_counts, names=category, title="Customer Statistics", ), output_type='div', include_plotlyjs=False)
    
    fig = admin_stats_plot = px.pie(values=category_counts, names=category, title="Customer Statistics", )
    fig.layout.update({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    admin_stats_plot = plot(fig, output_type='div', include_plotlyjs=False)

    return admin_stats_plot

