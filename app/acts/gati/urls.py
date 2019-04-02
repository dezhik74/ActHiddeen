from django.urls import path
from .views import *

urlpatterns = [
    path('', GatiOrderView.as_view(), name='gati_order_list_url')
    ]