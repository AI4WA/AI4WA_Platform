from django.contrib import admin
from crime.models import Crime
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Crime)
class CrimeAdmin(ImportExportModelAdmin):
    list_display = ("name", "count", "created_at", "updated_at")
    search_fields = ("name", "count")
    list_filter = ("created_at", "updated_at")
    fieldsets = (
        (
            "Crime Information",
            {
                "fields": (
                    "name",
                    "description",
                    "count",
                )
            },
        ),
    )
