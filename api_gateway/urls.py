from django.urls import path
from . import views

app_name='api_gateway'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
]