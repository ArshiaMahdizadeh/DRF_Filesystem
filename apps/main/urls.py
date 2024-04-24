from django.urls import path,include
from . import views

app_name="main"
urlpatterns = [
    path('create_user/', views.AdminCreateUserView.as_view(), name='admin_create_user'),
    path('view_users/', views.CustomUserGetView.as_view(), name='view_all'),
    path('file_upload/', views.UserFileUploadView.as_view(), name='file_upload'),
    path('my_files/', views.UserFilesView.as_view(), name='my_files'),
    path('delete_file/<int:pk>/', views.DeleteFileView.as_view(), name='delete_file'),
    path('delete_all_files/', views.DeleteAllFilesView.as_view(), name='delete_all_files'),
  
]
