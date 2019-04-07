from django.urls import path
from .views import *

urlpatterns = [
    path('', ks14_list, name='ks14_list_url'),
    path('view-<int:pk>', KS14_Detail.as_view(), name='ks14_object_detail_url'),
    path('edit-<int:pk>', object_edit, name='ks14_object_edit_url'),
    path('copy-<int:pk>', copy_ks14, name='ks14_copy_url'),
    path('delete-<int:pk>', delete_ks14, name='ks14_delete_url'),
    path('make_ks14-<int:pk>', make_ks14_docx, name='make_ks14_docx'),
    path('make_ks3-<int:pk>', make_ks3_xlsx, name='make_ks3_xlsx'),
    path('make_peresort-<int:pk>', make_peresort, name='make_peresort'),
    path('make_ks2-<int:pk>', make_ks2_xlsx, name='make_ks2_xlsx'),
]