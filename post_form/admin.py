from django.contrib import admin
from .models import FileUpload
from django.http import HttpResponse
import zipfile
import os
from django.conf import settings
from io import BytesIO
import logging
from django.core.files.storage import default_storage
import tempfile
from django.contrib import messages

logger = logging.getLogger(__name__)

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'has_files')
    actions = ['download_files_as_zip']

    def has_files(self, obj):
        return bool(obj.logo or obj.background_image or obj.banner)
    has_files.boolean = True
    has_files.short_description = 'Has Files'

    def download_files_as_zip(self, request, queryset):
        if not queryset.exists():
            messages.error(request, "No files selected.")
            return

        # Create a BytesIO object to store the ZIP file
        zip_buffer = BytesIO()
        files_added = 0
        
        try:
            # Create the ZIP file
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_upload in queryset:
                    logger.info(f"Processing upload {file_upload.id}")
                    
                    # Add logo if exists
                    if file_upload.logo:
                        try:
                            logger.info(f"Processing logo: {file_upload.logo}")
                            # Download file from Azure to a temporary file
                            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                # Download the file
                                with default_storage.open(str(file_upload.logo), 'rb') as source_file:
                                    temp_file.write(source_file.read())
                                temp_file.flush()
                                
                                # Add to ZIP
                                zip_file.write(
                                    temp_file.name,
                                    f'logos/{os.path.basename(str(file_upload.logo))}'
                                )
                                files_added += 1
                                logger.info(f"Added logo to ZIP: {file_upload.logo}")
                            os.unlink(temp_file.name)
                        except Exception as e:
                            logger.error(f"Error processing logo: {str(e)}")
                            messages.error(request, f"Error processing logo: {str(e)}")
                    
                    # Add background image if exists
                    if file_upload.background_image:
                        try:
                            logger.info(f"Processing background: {file_upload.background_image}")
                            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                # Download the file
                                with default_storage.open(str(file_upload.background_image), 'rb') as source_file:
                                    temp_file.write(source_file.read())
                                temp_file.flush()
                                
                                # Add to ZIP
                                zip_file.write(
                                    temp_file.name,
                                    f'background_images/{os.path.basename(str(file_upload.background_image))}'
                                )
                                files_added += 1
                                logger.info(f"Added background to ZIP: {file_upload.background_image}")
                            os.unlink(temp_file.name)
                        except Exception as e:
                            logger.error(f"Error processing background: {str(e)}")
                            messages.error(request, f"Error processing background: {str(e)}")
                    
                    # Add banner if exists
                    if file_upload.banner:
                        try:
                            logger.info(f"Processing banner: {file_upload.banner}")
                            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                                # Download the file
                                with default_storage.open(str(file_upload.banner), 'rb') as source_file:
                                    temp_file.write(source_file.read())
                                temp_file.flush()
                                
                                # Add to ZIP
                                zip_file.write(
                                    temp_file.name,
                                    f'banners/{os.path.basename(str(file_upload.banner))}'
                                )
                                files_added += 1
                                logger.info(f"Added banner to ZIP: {file_upload.banner}")
                            os.unlink(temp_file.name)
                        except Exception as e:
                            logger.error(f"Error processing banner: {str(e)}")
                            messages.error(request, f"Error processing banner: {str(e)}")

            # Get the size of the ZIP file
            zip_size = zip_buffer.tell()
            logger.info(f"ZIP file size: {zip_size} bytes")
            logger.info(f"Total files added to ZIP: {files_added}")

            if zip_size == 0:
                messages.warning(request, "No files were found to add to the ZIP.")
                return

            # Prepare the response
            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=archivos_descargados.zip'
            response['Content-Length'] = zip_size
            
            messages.success(request, f"Successfully added {files_added} files to ZIP.")
            return response

        except Exception as e:
            logger.error(f"Error creating ZIP file: {str(e)}")
            messages.error(request, f"Error creating ZIP file: {str(e)}")
            return
    
    download_files_as_zip.short_description = "Download selected files as ZIP"

admin.site.register(FileUpload, FileUploadAdmin)

