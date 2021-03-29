from django.contrib.auth.models import User
from django.db import connection
from django.contrib import messages
from django.shortcuts import render
from Banker.View.bankerlogin import bankerlogin

class FactoryPattern:

	def deletecustomer(request, username):
		"""
		Delete the customer based on the Username and update the same in the DB	
		"""
		if FactoryPattern.check_status(username) == 'nouser':
			messages.error(request, ('No such Customer exists.'))
		else:
			with connection.cursor() as cursor:
				results = cursor.execute("DELETE FROM public.auth_user where username = '%s'" %username)
				connection.commit()
			messages.success(request, ('Customer deleted successfully'))
		
		return render(request, 'Banker/customeradmin.html', {}) 

	def enablecustomer(request, username):
		"""
		Check whether the username is in disabled status to proceed with Enabling the customer based on the Username and update the same in the DB
		"""	
		if FactoryPattern.check_status(username) == 'True':
			messages.error(request, ('Customer is already in active status.'))
		elif FactoryPattern.check_status(username) == 'nouser':
			messages.error(request, ('No such Customer exists.'))
		elif FactoryPattern.check_status(username) == 'False':
			with connection.cursor() as cursor:
				results = cursor.execute("UPDATE public.auth_user SET is_active = 'true' where username = '%s'" %username)
				connection.commit()
			messages.success(request, ('Customer enabled successfully'))

		return render(request, 'Banker/customeradmin.html', {})

	def disablecustomer(request, username):
		"""
		Check whether the username is in enabled status to proceed with disabling the customer based on the Username and update the same in the DB
		"""		
		if FactoryPattern.check_status(username) == 'False':
			messages.error(request, ('Customer is already in disabled status.'))
		elif FactoryPattern.check_status(username) == 'nouser':
			messages.error(request, ('No such Customer exists.'))
		elif FactoryPattern.check_status(username) == 'True':
			with connection.cursor() as cursor:
				results = cursor.execute("UPDATE public.auth_user SET is_active = 'false' where username = '%s'" %username)
				connection.commit()
			messages.success(request, ('Customer disabled successfully'))

		return render(request, 'Banker/customeradmin.html', {})

	def check_status(username):
		"""
		Check whether the status based on username
		"""	
		with connection.cursor() as cursor:
			cursor.execute("SELECT is_active FROM public.auth_user WHERE username = '%s'" %username)
			user_status = cursor.fetchone()
			if cursor.rowcount == 0:
				user_status = 'nouser'
			else:
				i = ' '.join([str(elem) for elem in user_status])
				i = i.replace('(', '')
				i = i.replace(',)', '')
				user_status = i
				#print(user_status)

		return user_status
