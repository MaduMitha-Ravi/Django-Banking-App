from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import connection
from Banker.View.factorydesignpattern_bankeradmin import FactoryPattern

class abstract_bankeradministration:

	def admin(request, username):
		if request.POST.get('dropdown') == 'disablecustomer':
            FactoryPattern.disablecustomer(request, username)
        elif request.POST.get('dropdown') == 'deletecustomer': 
            FactoryPattern.deletecustomer(request, username)
        elif request.POST.get('dropdown') == 'enablecustomer': 
            FactoryPattern.enablecustomer(request, username)