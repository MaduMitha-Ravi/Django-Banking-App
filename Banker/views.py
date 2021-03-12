from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Banker.forms import RegisterCustomerForm
from Banker.models import RegisterCustomers
from django.contrib import messages
from django.contrib.auth import get_user_model
from Customer.forms import LoanRequestForm
from Customer.models import LoanRequest
from django.db import connection
import pandas as pd
from django.conf import settings

from Customer.views import Customer
#from Banker.observerdesignpattern import ObserverPattern
from Banker.View.observerdesignpattern_loanstatus import ObserverPattern
#from Banker.factorydesignpattern import FactoryPattern
from Banker.View.factorydesignpattern_bankeradmin import FactoryPattern
from Banker.View.machinelearning import machinelearning
from Banker.View.bankerlogin import bankerlogin
from Banker.View.registernewcustomers import registernewcustomers
from Banker.View.loanrequestqueue import loanrequestqueue
from Banker.View.bankeradministration import bankeradministration


class Banker:

    def banker_login(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if bankerlogin.is_user_admin(request, username) == 'True':
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    form = RegisterCustomerForm()
                    return HttpResponseRedirect('/Banker/registercustomer/')
                else:
                    messages.error(request, ('Incorrect credentials!'))
                    return render(request, 'Banker/banker_login.html', {})
            elif bankerlogin.is_user_admin(request, username)  == '':
                messages.error(request, ('User does not exist!'))
        return render(request, 'Banker/banker_login.html', {})

    @login_required(login_url='/Banker/banker_login/')
    def registercustomer(request):

        return registernewcustomers.registercustomer(request)

    @login_required(login_url='/Banker/banker_login/')
    def loanrequest(request):
        
        if request.POST:
            if 'approve_loan' in request.POST:
                loanrequestqueue.loan_status_update_approve(request)
            elif 'decline_loan' in request.POST:
                loanrequestqueue.loan_status_update_decline(request)
            elif 'loan_prediction' in request.POST:
                loanrequestqueue.loan_prediction(request)
        
        table = LoanRequest.objects.all().filter(loan_status = 'Decision Pending')
            
        return render(request, 'Banker/loanrequest.html', {'table': table})


    @login_required(login_url='/Banker/banker_login/')
    def customeradmin(request):
        admin_stats_plot = bankeradministration.admin_stats(request)
        context = {'admin_stats_plot': admin_stats_plot}
        print('in main')
        if request.POST:
            print('in post')
            username = request.POST.get('username')
            if bankeradministration.validate_username(request, username) == 0:
                abstract_bankeradministration.admin(request, username)
                

                admin_stats_plot = bankeradministration.admin_stats(request)
                context = {'admin_stats_plot': admin_stats_plot}

                return render(request, 'Banker/customeradmin.html', {'admin_stats_plot': admin_stats_plot})
        else:
            return render(request, 'Banker/customeradmin.html', {'admin_stats_plot': admin_stats_plot})

    @login_required(login_url='/Banker/banker_login/')
    def banker_logout(request):
        logout(request)
        return render(request, 'Banker/banker_logout.html', {})


    








