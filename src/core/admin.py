from django.contrib import admin

from core.models import Position, Worker


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_max_show_all = 20
    show_full_result_count = True
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_max_show_all = 20
    show_full_result_count = True
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'position',
        'is_active',
    )
    list_editable = (
        'position',
        'is_active',
    )
    search_fields = (
        'last_name',
        'first_name',
        'position__name',
    )
    list_filter = (
        'is_active',
        'position__name',
        'hired_date',
    )
    readonly_fields = ('hired_date', 'updated_at')
