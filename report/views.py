from django.shortcuts import render
from django.http import HttpResponse
from .report import doc_write, report_write


from . import views
import pandas as pd
import csv
# Create your views here.


def index(request):
    context={
    }
    return render(request,'report/report_list.html', context)


def detail(request):
    context = {
    }
    return render(request,'report/report_detail.html', context)
    #return HttpResponse("보고서 상세")




