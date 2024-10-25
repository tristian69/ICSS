from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.template import loader

from IPython.display import display

from . import views
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

# Create your views here.

def index(request):
    context = {
    }
    return render(request, 'monitoring/monitoring_list.html', context)



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
    context={ response }
    return render(request, context)


def detail(request):
    context = {

    }

    return render(request, 'monitoring/monitoring_detail.html', context)
    #return HttpResponse(" 모니터링 상세 ")