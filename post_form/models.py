from django.db import models

# Create your models here.

class WebDesignRequest(models.Model):
    client_name = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    additional_resources = models.TextField(verbose_name="Recursos Adicionales", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud de {self.client_name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Solicitud de Diseño Web"
        verbose_name_plural = "Solicitudes de Diseño Web"

class WebDesignFile(models.Model):
    FILE_TYPES = [
        ('logo', 'Logo'),
        ('banner', 'Banner'),
        ('icons', 'Iconos'),
        ('images', 'Imágenes'),
        ('videos', 'Videos'),
    ]

    request = models.ForeignKey(WebDesignRequest, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='client_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.file.name}"

    class Meta:
        verbose_name = "Archivo de Diseño Web"
        verbose_name_plural = "Archivos de Diseño Web"
