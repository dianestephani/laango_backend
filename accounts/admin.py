from django.contrib import admin
from .models import InterpreterProfile


@admin.register(InterpreterProfile)
class InterpreterProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email_address', 'phone_number', 'city', 'state', 'dshs_certified', 'languages_spoken']
    list_filter = ['state', 'dshs_certified', 'spanish', 'russian', 'portuguese', 'mandarin', 'somali', 'farsi', 'vietnamese', 'amharic', 'tigrinya']
    search_fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'city']

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'email_address')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'zip_code')
        }),
        ('Certification', {
            'fields': ('dshs_certified',)
        }),
        ('Languages Spoken', {
            'fields': ('amharic', 'farsi', 'mandarin', 'portuguese', 'russian', 'somali', 'spanish', 'tigrinya', 'vietnamese'),
            'classes': ('collapse',)
        }),
    )

    def languages_spoken(self, obj):
        """Display languages spoken in the list view"""
        languages = obj.get_languages()
        return ', '.join(languages) if languages else 'None'
    languages_spoken.short_description = 'Languages'
