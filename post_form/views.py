from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FileUpload
from django.views.generic import CreateView
from django.urls import reverse_lazy

class FileUploadView(CreateView):
    model = FileUpload
    template_name = 'post_form/files_form.html'
    success_url = reverse_lazy('post_form:file_upload_success')
    fields = ['logo', 'background_image', 'banner']
    
    def form_valid(self, form):
        messages.success(self.request, 'Files uploaded successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'There was an error uploading the files. Please try again.')
        return super().form_invalid(form)

def file_upload_success(request):
    return render(request, 'post_form/upload_success.html')
