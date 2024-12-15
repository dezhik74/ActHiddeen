from django.contrib import admin
from django.urls import path
from django.urls import include
from django.shortcuts import render


urlpatterns = [
    path('', include('hiddenactsbase.urls')),
    path('admin/', admin.site.urls, name='admin_url'),
    ]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
