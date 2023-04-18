from django.urls import path
from .views import ObjectsList, object_edit, ObjectDetail, ObjectTableView, \
    copy_object, delete_object, make_word_file, make_cert_file

urlpatterns = [
    path('', ObjectsList.as_view(), name='objects_list_url'),
    path('edit-<int:pk>/', object_edit, name='object_edit_url'),
    path('see-<int:pk>/', ObjectDetail.as_view(), name='object_detail_url'),
    path('table-<int:pk>/', ObjectTableView.as_view(), name='object_table_url'),
    path('copy-<int:pk>', copy_object, name='copy_object'),
    path('obj_delete-<int:pk>', delete_object, name='delete_object'),
    path('make_word-<int:pk>', make_word_file, name='make_word_file'),
    path('make_sert-<int:pk>', make_cert_file, name='make_cert_file'),

    ]