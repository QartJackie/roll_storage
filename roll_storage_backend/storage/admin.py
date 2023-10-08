from django.contrib import admin

from storage.models import Coil


class CoilAdmin(admin.ModelAdmin):
    """Представление модели рулона в админке."""

    list_display = (
        'id',
        'length',
        'weight',
        'add_date',
        'deletion_date',
    )
    list_filter = (
        'length',
        'weight',
        'add_date',
        'deletion_date',
    )
    search_fields = (
        'add_date',
        'deletion_date',
    )


admin.site.register(Coil, CoilAdmin)
