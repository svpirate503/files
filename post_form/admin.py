from django.urls import path
from django.http import HttpResponse, Http404
from django.contrib import admin
from django.utils.html import format_html
from django.core.files.storage import default_storage
from zipfile import ZipFile
from io import BytesIO

from .models import WebDesignRequest, WebDesignFile


class WebDesignFileInline(admin.TabularInline):
    model = WebDesignFile
    extra = 0
    readonly_fields = ('uploaded_at',)
    fields = ('file_type', 'file', 'uploaded_at')

@admin.register(WebDesignRequest)
class WebDesignRequestAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_at', 'updated_at', 'get_file_count', 'download_files_link')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('client_name', 'additional_resources')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WebDesignFileInline]
    
    def get_file_count(self, obj):
        return obj.files.count()
    get_file_count.short_description = 'Archivos'

    def download_files_link(self, obj):
        if obj.files.exists():
            return format_html(
                '<a class="button" href="{}">📦 Descargar ZIP</a>',
                f'./download/{obj.pk}/'
            )
        return "Sin archivos"
    download_files_link.short_description = "Descargar Archivos"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download/<int:pk>/', self.admin_site.admin_view(self.download_zip), name="webdesign_download_zip")
        ]
        return custom_urls + urls

    def download_zip(self, request, pk):
        try:
            obj = WebDesignRequest.objects.get(pk=pk)
        except WebDesignRequest.DoesNotExist:
            raise Http404("No se encontró la solicitud")

        buffer = BytesIO()
        with ZipFile(buffer, "w") as zip_file:
            for file_obj in obj.files.all():
                if file_obj.file:
                    file_name = file_obj.file.name.split('/')[-1]
                    file_content = default_storage.open(file_obj.file.name).read()
                    zip_file.writestr(f"{file_obj.file_type}/{file_name}", file_content)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename=archivos_{obj.client_name}.zip'
        return response

@admin.register(WebDesignFile)
class WebDesignFileAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'file_type', 'file', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('request__client_name', 'file')
    readonly_fields = ('uploaded_at',)
    
    def get_client_name(self, obj):
        return obj.request.client_name
    get_client_name.short_description = 'Cliente'
    get_client_name.admin_order_field = 'request__client_name'


