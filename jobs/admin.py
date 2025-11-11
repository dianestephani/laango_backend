from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['languages_needed', 'job_type', 'date', 'time', 'full_address', 'assigned_interpreter', 'status', 'payment', 'mileage_included', 'requires_dshs_certification', 'created_at']
    list_filter = ['status', 'job_type', 'date', 'state', 'requires_dshs_certification', 'mileage_included', 'assigned_interpreter', 'spanish', 'russian', 'portuguese', 'mandarin', 'somali', 'farsi', 'vietnamese', 'amharic', 'tigrinya']
    search_fields = ['street_address', 'city', 'state', 'zip_code', 'assigned_interpreter__first_name', 'assigned_interpreter__last_name']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']

    fieldsets = (
        ('Job Details', {
            'fields': ('job_type', 'date', 'time', 'status', 'assigned_interpreter')
        }),
        ('Location', {
            'fields': ('street_address', 'city', 'state', 'zip_code')
        }),
        ('Languages Needed', {
            'fields': ('amharic', 'farsi', 'mandarin', 'portuguese', 'russian', 'somali', 'spanish', 'tigrinya', 'vietnamese'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('payment', 'mileage_included')
        }),
        ('Requirements', {
            'fields': ('requires_dshs_certification',)
        }),
    )

    def full_address(self, obj):
        """Display full address in the list view"""
        return f"{obj.street_address}, {obj.city}, {obj.state} {obj.zip_code}"
    full_address.short_description = 'Location'

    def languages_needed(self, obj):
        """Display languages needed in the list view"""
        languages = obj.get_languages()
        return ', '.join(languages) if languages else 'None'
    languages_needed.short_description = 'Languages'
