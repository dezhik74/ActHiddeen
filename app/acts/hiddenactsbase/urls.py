from django.urls import path
from .views import *

urlpatterns = [
    path('', ObjectsList.as_view(), name='objects_list_url'),
    path('edit-<int:pk>/', ObjectEdit.as_view(), name='object_edit_url'),
    path('see-<int:pk>/', ObjectDetail.as_view(), name='object_detail_url'),
    ]
