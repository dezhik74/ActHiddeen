from django.urls import path
from .views import *

urlpatterns = [
    path('', acts_list, name = 'acts_list_url'),
    path('object/<int:pk>/',act_detail, name='act_detail_url'),
]
