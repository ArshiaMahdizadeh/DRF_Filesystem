from django.contrib import admin
from.models import CustomUser, FileUpload

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_active', 'is_admin', 'is_superuser')
    search_fields = ('mobile_number', 'email', 'name', 'family')

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'upload_date')
    search_fields = ('user__mobile_number', 'file')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FileUpload, FileUploadAdmin)