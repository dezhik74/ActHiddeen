from django.urls import path
from .views import *

urlpatterns = [
    path('', ks14_list, name='ks14_list_url'),
    path('view-<int:pk>', KS14_Detail.as_view(), name='ks14_object_detail_url'),
    path('edit-<int:pk>', object_edit, name='ks14_object_edit_url'),
]