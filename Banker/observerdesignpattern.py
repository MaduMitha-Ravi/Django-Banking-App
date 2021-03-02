from twilio.rest import Client
import keyboard
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from Customer.views import customermainpage

class ObserverPattern:

    def __init__(self, request, loan_message):

        self.customer_id = ''
        self.request = request
        self.loan_message = loan_message
        #print(loan_message)
        self.attach_customer()

    def attach_customer(self):
        
        self.customer_id = self.request.user.pk
        #print(self.customer_id)
        self.notify_customer()

    def detach_customer(self):
        
        self.customer_id = ''

    def notify_customer(self):
        
        customer_emailid = self.request.user.email

        customer_contactnumber = "+16399978200"
        #customer_contactnumber = get_contactnumber(request)
        #customer_contactnumber = User.objects.get(username=request.user.username).contactnumber

        self.email_alert(customer_emailid)
        print("email sent")
        self.msg_alert(customer_contactnumber)
        print("text msg sent")

        self.update_customerview()

    def update_customerview(self):
        customermainpage(self.request) 
        self.detach_customer()

    def msg_alert(self, customer_contactnumber):
        #client = Client("AC63e7f70f70cfef1f11ff4959c858b432", "d3c269c2cee5c10ec3c5dd970c54810d")

        # Get status of loan 

        if self.loan_message == 'Approved':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(to=["+16399978200", "+13065192658" ],
                                           from_="+15157580580", 
                                           body="Congratulations! Your Loan is Approved.")

        elif self.loan_message == 'Declined':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(to=["+16399978200", "+13065192658"  ],
                               from_="+15157580580", 
                               body="Sorry, your loan application is Declined.")


    def email_alert(self, customer_emailid):

        email_from = settings.EMAIL_HOST_USER
        customer_emailid = ['cuteberry.madhu@gmail.com', 'surambipinkumar@gmail.com',]
        

        if self.loan_message == 'Approved':
            subject = 'Congratulations! Your Loan is Approved.'
            message = "Congratulations! Your Loan is Approved."
            send_mail( subject, message, email_from, customer_emailid)

        elif self.loan_message == 'Declined':
            subject = 'Sorry, your loan application is Declined.'
            message = "Sorry, your loan application is Declined."
            send_mail( subject, message, email_from, customer_emailid)


    def get_contactnumber(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT contactnumber FROM public.\"Banker_registercustomers\" where username = '%s'" %self.request.user.username)
            contactnumber = cursor.fetchone()
            print(contactnumber)
            i = ' '.join([str(elem) for elem in contactnumber])
            i = i.replace('(', '')
            i = i.replace('\'', '')
            i = i.replace(',)', '')
            contactnumber = i

            print(contactnumber)

        return contactnumber

    