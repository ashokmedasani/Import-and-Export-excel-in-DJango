from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import person

#  Register your models here.

@admin.register(person)
class personadmin(ImportExportModelAdmin):
    list_display = ('Name','Age','Contact')
    