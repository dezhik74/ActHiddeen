from django.urls import path

from hiddenactsbase import views

urlpatterns = [
    path('', views.main_index, name='main_index'),
    path('list/', views.ObjectsList.as_view(), name='objects_list_url'),
    path('edit-<int:pk>/', views.object_edit, name='object_edit_url'),
    path('see-<int:pk>/', views.ObjectDetail.as_view(), name='object_detail_url'),
    path('table-<int:pk>/', views.ObjectTableView.as_view(), name='object_table_url'),
    path('copy-<int:pk>', views.copy_object, name='copy_object'),
    path('obj_delete-<int:pk>', views.delete_object, name='delete_object'),
    path('make_word-<int:pk>', views.make_word_file, name='make_word_file'),
    path('make_sert-<int:pk>', views.make_cert_file, name='make_cert_file'),
    path('new-edit/<int:pk>/', views.new_object_edit, name='new_object_edit'),
    path('api/get-object/<int:pk>/', views.get_object, name='get_object'),
    path('api/get-all-objects/', views.get_all_objects, name='get_all_objects'),
    path('api/results/', views.save_object, name='save_object'),
    path('api/get-object-acts/<int:pk>/', views.get_object_acts, name='get_object_acts'),
    ]
