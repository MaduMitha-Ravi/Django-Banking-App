from django.conf.urls import url
from Banker import views
# SET THE NAMESPACE!

app_name = 'Banker'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^banker_login/$',views.banker_login,name='banker_login'),
    url(r'^registercustomer/$',views.registercustomer,name='registercustomer'), #form
    url(r'^banker_logout/$',views.banker_logout,name='banker_logout'),
    url(r'^loanrequest/$',views.loanrequest,name='loanrequest'),
    url(r'^loanrequest/$',views.loan_status_update_approve,name='loan_status_update_approve'),
    url(r'^loanrequest/$',views.loan_status_update_decline,name='loan_status_update_decline'),
    url(r'^loanrequest/$',views.loan_prediction,name='loan_prediction'),
    url(r'^customeradmin/$',views.customeradmin,name='customeradmin'),
   # url(r'^customeradmin/$',views.disablecustomer,name='disablecustomer'),
   # url(r'^customeradmin/$',views.deletecustomer,name='deletecustomer'),
   # url(r'^customeradmin/$',views.enablecustomer,name='enablecustomer'),
   # url(r'broadcast$', views.msg_alert, name="msg_alert"),
]