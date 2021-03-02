class ObserverPattern(request, loan_message):

"""Observer Pattern is called when an update happens on the decision of the loan 
request which calls for a set of activities to happen for the subscribers 
(loan request owners) based on the status (loan message)"""

	customer_id = ''
	request = request
	loan_message = loan_message

	attach_customer(request, customer_id, loan_message)

def attach_customer(request, customer_id, loan_message):
"""
Customer ID for which the loan status update needs to be sent is added
"""
	customer_id = request.user.pk
	notify_customer(request, customer_id, loan_message)

def notify_customer(request, customer_id, loan_message):
"""
Based on the Customer ID Email ID and Contact number are captured
Email Alert and Text Alert using Twilio is sent
"""
	customer_emailid = request.user.email
    customer_contactnumber = get_contactnumber(request)
	
	email_alert(request, customer_emailid, loan_message)
   	msg_alert(request, customer_contactnumber, loan_message)
	update_customerview(request)

def email_alert(request, customer_emailid, loan_message):
"""
Email Alert for the loan status update
"""
	if loan_message == 'Approved':
		'send_alert'
	elif loan_message == 'Declined':
	 	'send_alert'

def msg_alert(request, customer_contactnumber, loan_message):
"""
Text Alert for the loan status update using Twilio
"""
	if loan_message == 'Approved':
		'send_alert'
	elif loan_message == 'Declined':
	 	'send_alert'

def update_customerview(request):
"""
Customer's view or main page gets updated according to status update
"""
	customermainpage(request) 
    detach_customer(request)
	
def customermainpage(request):
"""
Customer's view or main page gets updated according to status update
"""
	'update_loan_status'

def detach_customer(request):
"""
Customer ID is removed once the loan status changes are notified
"""
	customer_id = ''



class FactoryPattern:

	def deletecustomer(request, username):
	"""
	Delete the customer based on the Username and update the same in the DB	
	"""
		'delete_from_db'
		messages.success(request, ('Customer deleted successfully'))

		return render(request, 'Banker/customeradmin.html', {}) 

	def enablecustomer(request, username):
	"""
	Check whether the username is in disabled status to proceed with Enabling the customer based on the Username and update the same in the DB
	"""	
		if check_status(username) == 'true':
			messages.success(request, ('Customer is already in active status.'))
		elif check_status(username) == 'false':
			'update_db'
			messages.success(request, ('Customer enabled successfully'))

		return render(request, 'Banker/customeradmin.html', {})

	def disablecustomer(request, username):
	"""
	Check whether the username is in enabled status to proceed with disabling the customer based on the Username and update the same in the DB
	"""		
		if FactoryPattern.check_status(username) == 'False':
			messages.success(request, ('Customer is already in disabled status.'))
		elif FactoryPattern.check_status(username) == 'True':
			'update_db'
			messages.success(request, ('Customer disabled successfully'))

		return render(request, 'Banker/customeradmin.html', {})

	def check_status(username):
	"""
	Check whether the status based on username
	"""	
		'get_username_status_from_DB'		

		return user_status
		