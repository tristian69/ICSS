from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import path
from IPython.display import display
from .dashboard import dash_read

from . import views
#form .dashboard import station

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import csv
import os

# Create your views here.

f=open("static/관세청_HSK별_신성질별_성질별_분류_20240101.csv", 'r', encoding='cp949')
l=[]
lines = f.readlines()
for line in lines:
    l.append(line.split(','))
    print(line)
    f.close()

    data = l[1:11]

def index(request):
    context = {'data': data}
    return render(request, 'dashboard/dashboard_list.html', context)



def index_bak(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ("First row", "Foo", "Bar", "Baz"),
        ("Second row", "A", "B", "C", '"Testing"', "Here's a quote"),
    )

    t = loader.get_template("my_template_name.txt")
    c = {"data": csv_data}
    response.write(t.render(c))
    return response
    #return render(request, 'dashboard/dashboard_list.html')
    #return HttpResponse("대시보드")


def detail(request):
    context = {

    }

    return render(request, 'dashboard/dashboard_detail.html', context)
    #return HttpResponse("대시보드")
