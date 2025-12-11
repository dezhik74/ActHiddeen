from django.urls import path

from water import views

app_name = 'water'

urlpatterns = [
    path('list/', views.WaterAssayListView.as_view(), name='assay_list'),
    path('create/', views.WaterAssayCreateView.as_view(), name='assay_create'),
    path('<int:pk>/update/', views.WaterAssayUpdateView.as_view(), name='assay_update'),
    path('<int:pk>/copy/', views.WaterAssayCopyView.as_view(), name='assay_copy'),
    path('<int:pk>/delete/', views.WaterAssayDeleteView.as_view(), name='assay_delete'),
    path('<int:pk>/download-docx/', views.generate_water_docx, name='assay_download_docx'),
]