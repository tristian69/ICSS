from django.shortcuts import render
from .api import check_air

# Create your views here.

def index(request):
    res = check_air()
    pm10 = res.get('동작대로 중앙차로')
    context = { 'station': '동작대로 중앙차로', 'pm10': pm10, 'dust': res}
    return render(request, 'api_gateway/api_gateway_list.html', context)

def detail(request):
    res = check_air()
    context = {'dust': res}
    return render(request, 'api_gateway/api_gateway_detail.html', context)