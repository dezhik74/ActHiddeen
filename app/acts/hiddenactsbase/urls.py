from django.urls import path
from .views import *

urlpatterns = [
    path('', ObjectsList.as_view(), name='objects_list_url'),
    path('edit-<int:pk>/', object_edit, name='object_edit_url'),
    path('see-<int:pk>/', ObjectDetail.as_view(), name='object_detail_url'),
    path('create_hidden_to_end-<int:pk>/', create_hidden_act_to_end, name='create_hidden_act_to_end'),
    path('create_blow_down-<int:pk>/', create_blow_down, name='create_blow_down'),
    path('delete-<int:pk_obj>-<int:pk_act>', delete_hidden_act, name='delete_hidden_act'),
    path('delete_blow_down-<int:pk>', delete_blow_down_act, name='delete_blow_down_act'),
    path('copy-<int:pk>', copy_object, name='copy_object'),
    path('obj_delete-<int:pk>', delete_object, name='delete_object'),
    path('make_word-<int:pk>', make_word_file, name='make_word_file')
    ]