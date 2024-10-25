"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from iils.views import base_views

app_name ='iils'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('iils/', include('iils.urls')),
    path('common/', include('common.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('mapping/', include('mapping.urls')),
    path('report/', include('report.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api_gateway/', include('api_gateway.urls')),
    path('', base_views.index, name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # static 경로 추가
