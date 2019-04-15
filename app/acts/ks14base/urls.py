from django.urls import path
from .views import *

urlpatterns = [
    path('', ks14_list, name='ks14_list_url'),
    path('view-<int:pk>', KS14_Detail.as_view(), name='ks14_object_detail_url'),
    path('structure-<int:pk>', ks14_object_edit_structure, name='ks14_object_edit_structure_url'),
    path('edit-<int:pk>', ks14_object_edit, name='ks14_object_edit_url'),
    path('copy-<int:pk>', copy_ks14, name='ks14_copy_url'),
    path('delete-<int:pk>', delete_ks14, name='ks14_delete_url'),
    path('make_ks14-<int:pk>-<int:pk2>', make_ks14_docx, name='make_ks14_docx'),
    path('make_ks3-<int:pk>-<int:pk2>', make_ks3_xlsx, name='make_ks3_xlsx'),
    path('make_peresort-<int:pk>-<int:pk2>', make_peresort, name='make_peresort'),
    path('make_ks2-<int:pk>-<int:pk2>', make_ks2_xlsx, name='make_ks2_xlsx'),
    path('insert_act-<int:pk>', insert_act, name='insert_act_url'),
    path('delete_act-<int:pk>-<int:pk2>', delete_act, name='delete_act_url'),
]