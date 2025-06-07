from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from datetime import datetime

def validate_file_size(value):
    filesize = value.size
    
    if value.field.name == 'file':
        file_type = value.instance.file_type if hasattr(value.instance, 'file_type') else None
        
        if file_type == 'videos':
            if filesize > 500 * 1024 * 1024:  # 500MB
                raise ValidationError("Maximum size for videos is 500MB")
        elif file_type in ['logo', 'banner', 'images']:
            if filesize > 100 * 1024 * 1024:  # 100MB
                raise ValidationError("Maximum size for images is 100MB")
        elif file_type == 'icons':
            if filesize > 50 * 1024 * 1024:  # 50MB
                raise ValidationError("Maximum size for icons is 50MB")

def get_upload_path(instance, filename):
    # Obtener la extensión del archivo
    ext = os.path.splitext(filename)[1]
    # Crear un nombre único para el archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Crear la ruta basada en el tipo de archivo y el nombre del cliente
    return f'uploads/{instance.file_type}/{instance.request.client_name}/{timestamp}{ext}'

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.mp4', '.webm', '.mov']:
        raise ValidationError('Unsupported file type. Please upload an image or video file.')

# Create your models here.

class WebDesignRequest(models.Model):
    client_name = models.CharField(max_length=200, verbose_name="Client Name")
    additional_resources = models.TextField(verbose_name="Additional Resources", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request from {self.client_name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Web Design Request"
        verbose_name_plural = "Web Design Requests"

class WebDesignFile(models.Model):
    FILE_TYPES = [
        ('logo', 'Logo'),
        ('banner', 'Banner'),
        ('icons', 'Icons'),
        ('images', 'Images'),
        ('videos', 'Videos'),
    ]

    request = models.ForeignKey(WebDesignRequest, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(
        upload_to=get_upload_path,
        validators=[validate_file_size],
        help_text="Maximum sizes: Videos (500MB), Images (100MB), Icons (50MB)",
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.file:
            validate_file_size(self.file)

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.file.name if self.file else 'No file'}"

    class Meta:
        verbose_name = "Web Design File"
        verbose_name_plural = "Web Design Files"

class ClientRequest(models.Model):
    client_name = models.CharField(max_length=100)
    additional_resources = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.client_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class FileUpload(models.Model):
    logo = models.ImageField(upload_to='uploads/logos/', null=True, blank=True)
    background_image = models.ImageField(upload_to='uploads/backgrounds/', null=True, blank=True)
    banner = models.ImageField(upload_to='uploads/banners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"File Upload {self.id} - {self.created_at}"

    class Meta:
        verbose_name = "File Upload"
        verbose_name_plural = "File Uploads"
