from django.shortcuts import render
from Banker.forms import UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import connection


import pandas as pd
import numpy as np
from plotly.graph_objs import *
import plotly.express as px
from plotly.offline import plot
from django.conf import settings

from Banker.View.bankerlogin import bankerlogin


class bankeradministration:

	def validate_username(request, username):
	    if len(username) != 0: 
	        if bankerlogin.is_user_customer(request, username) == 0:
	            messages.warning(request, ('Please enter valid username!'))
	        else:
	            return 0
	    elif len(username) == 0: 
	        messages.warning(request, ('Please enter username before proceeding!'))


	def admin_stats(request):
	    
	    category = ['Inactive Customers', 'Active Customers']
	    category_counts = []

	    with connection.cursor() as cursor:
	        cursor.execute("SELECT count(is_active) FROM public.auth_user group by is_active")
	        category_count = cursor.fetchall()

	        for i in category_count:
	            i = ' '.join([str(elem) for elem in i])
	            i = i.replace('(', '')
	            i = i.replace(',)', '')
	            category_counts.append(int(i))

	    #admin_stats_plot = plot(px.pie(values=category_counts, names=category, title="Customer Statistics", ), output_type='div', include_plotlyjs=False)
	    
	    fig = admin_stats_plot = px.pie(values=category_counts, names=category, color=category,
             color_discrete_map={'Inactive Customers':'cyan',
                                 'Active Customers':'royalblue',
                                 }, width=450, height=450,)
	    fig.layout.update({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
	    admin_stats_plot = plot(fig, output_type='div', include_plotlyjs=False)

	    return admin_stats_plot
