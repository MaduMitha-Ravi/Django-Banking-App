from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Banker.forms import RegisterCustomerForm
from Banker.models import RegisterCustomers
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import connection
from Banker.View.bankerlogin import bankerlogin


class registernewcustomers:


	@login_required(login_url='/Banker/banker_login/')
	def registercustomer(request):
		
		if request.method == 'POST':
			form = RegisterCustomerForm(request.POST)
			print(request.POST)
			if 'submit' in request.POST:
				if form.is_valid():
					UserModel = get_user_model()
					username = request.POST.get('username')
					password = request.POST.get('password')
					first_name = request.POST.get('firstname')
					last_name = request.POST.get('lastname')
					email = request.POST.get('email')
					if bankerlogin.is_user_customer(request, username) == 0:
						user = UserModel.objects.create_user(username=username, password = password, first_name=first_name, last_name=last_name, email = email)
						user.save()
						output = form.save()
						messages.success(request, ('Customer Registration successful! Customer ID is %s') % output.account_id)

						return render(request, 'Banker/registercustomer.html', {'form': form})
					else:
						messages.success(request, ('Username %s is not available') % output.username)
						#return render(request, 'Banker/registercustomer.html', {'form': form})
					
			elif 'reset' in request.POST:
				#form = RegisterCustomerForm()
				return HttpResponseRedirect(request.path)
		else:
			form = RegisterCustomerForm()
		
		return render(request, 'Banker/registercustomer.html', {'form': form})
