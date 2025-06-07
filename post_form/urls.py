from django.urls import path
from . import views

app_name = 'post_form'

urlpatterns = [
    path('', views.FileUploadView.as_view(), name='file_upload'),
    path('upload/success/', views.file_upload_success, name='file_upload_success'),
        ]
