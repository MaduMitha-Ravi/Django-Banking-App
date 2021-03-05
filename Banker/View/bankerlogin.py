from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import connection

class bankerlogin:


	def is_user_admin(request, username):
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
				
		return user_status

	def is_user_customer(request, username):
		with connection.cursor() as cursor:
			cursor.execute("SELECT account_id FROM public.\"Banker_registercustomers\" WHERE username = %s", [username])
			rowcount = cursor.rowcount
			connection.close()
			return rowcount