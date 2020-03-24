"""acts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.shortcuts import render


def main_index(request):
    return render(request, 'index_main.html')

urlpatterns = [
    path('',main_index,name='main_index'),
    path('admin/', admin.site.urls, name='admin_url'),
    path('actbase/', include('hiddenactsbase.urls'),name='actbase_url'),
    # path('ks14base/', include('ks14base.urls'),name='ks14base_url'),
    path('gati/', include('gati.urls'),name='gati_url'),
    ]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
