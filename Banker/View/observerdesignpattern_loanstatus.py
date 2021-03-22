from twilio.rest import Client
#import keyboard
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from Customer.views import Customer
#from Customer.views import customermainpage
from django.db import connection

class ObserverPattern:

    def __init__(self, request, loan_message):

        self.customer_id = ''
        self.request = request
        self.loan_message = loan_message
        self.attach_customer()

    def attach_customer(self):
        
        self.customer_id = self.request.user.pk
        #print(self.customer_id)
        ObserverAbstract.notify_customer(self)

    def detach_customer(self):
        
        self.customer_id = ''


class Subscriber:

    def get_subscriber_details(self):
        
        self.customer_emailid = ['cuteberry.madhu@gmail.com', 'surambipinkumar@gmail.com',]
        self.customer_contactnumber = ["+16399978200", "+13065192658" ]

        return self.customer_emailid, self.customer_contactnumber     


class ObserverAbstract:

    def notify_customer(self):
        
        self.customer_emailid, self.customer_contactnumber = Subscriber.get_subscriber_details(self)
        ObserverAlerts.email_alert(self,self.customer_emailid)
        ObserverAlerts.msg_alert(self,self.customer_contactnumber)
        
        ObserverAlerts.update_customerview(self)

class ObserverAlerts:

    def update_customerview(self):
        Customer.customermainpage(self.request) 
        ObserverPattern.detach_customer(self)

    def msg_alert(self, customer_contactnumber):
        

        if self.loan_message == 'Approved':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(to=customer_contactnumber,
                                           from_="+15157580580", 
                                           body="Congratulations! Your Loan is Approved.")

        elif self.loan_message == 'Declined':
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(to=customer_contactnumber,
                               from_="+15157580580", 
                               body="Sorry, your loan application is Declined.")


    def email_alert(self, customer_emailid):

        email_from = settings.EMAIL_HOST_USER

        if self.loan_message == 'Approved':
            subject = 'Congratulations! Your Loan is Approved.'
            message = "Congratulations! Your Loan is Approved with 82 percent accuracy."
            print(subject, message, email_from, customer_emailid)
            send_mail( subject, message, email_from, customer_emailid)

        elif self.loan_message == 'Declined':
            subject = 'Sorry, your loan application is Declined.'
            message = "Sorry, your loan application is Declined with 82 percent accuracy."
            print(subject, message, email_from, customer_emailid)
            send_mail( subject, message, email_from, customer_emailid)


    

    
