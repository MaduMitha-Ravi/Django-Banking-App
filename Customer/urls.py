from django.conf.urls import url, include
from Customer import views
# SET THE NAMESPACE!

from django.views.generic import TemplateView
from django.urls import path


from django.conf import settings
from django.conf.urls.static import static


app_name = 'Customer'
# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^customer_login/$',views.customer_login,name='customer_login'),
    url(r'^customer_logout/$',views.customer_logout,name='customer_logout'),
    url(r'^applyloan/$',views.applyloan,name='applyloan'),
    url(r'^stocktrading/$',views.stocktrading,name='stocktrading'),
    url(r'^stocktrading/$',views.stock_buy_sell,name='stock_buy_sell'),
    url(r'^customermainpage/$',views.customermainpage,name='customermainpage'),
    #url(r'^stocktrading/$',views.display_graph,name='display_graph'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    #url(r'^django_plotly_dash/', include('django_plotly_dash.urls')),
	
   # path('form/model', showform, name='showform'),
]