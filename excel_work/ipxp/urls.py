from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index' ),
    path('uploadfile/', views.uploadfile,  name='uploadfile'),
    path('display_data/', views.display_data,  name='display_data'),
    path('demodata/', views.simple_upload, name ='simple_upload' ),
    path('upload_excel/', views.upload_excel, name ='upload_excel' ),
    path('merge_excel/', views.merge_excel, name ='merge_excel' ),
    path('delete/<int:file_id>/', views.delete_excel, name='delete_excel'),
    path('upload_separate_excel/', views.upload_separate_excel, name ='upload_separate_excel' ),
    # path('delete/<int:file_id>/', views.delete_separate_excel, name='delete_separate_excel'),
    path('upload_separate_success/', views.upload_separate_success, name ='upload_separate_success' ),
    path('upload_form/', views.process_excel, name='upload_form'),
    path('media/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('file-list/', views.file_list, name='file_list'),
    path('merge_success/', views.merge_data, name='merge_data'),
    path('merge_error/', views.merge_error, name='merge_error'),
    path('delete-file/<path:merged_file_path>', views.delete_merged_file, name='delete_merged_file'),  # Add this line
]