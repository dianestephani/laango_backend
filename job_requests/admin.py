from django.contrib import admin
from .models import InterpreterContact


@admin.register(InterpreterContact)
class InterpreterContactAdmin(admin.ModelAdmin):
    list_display = ['job', 'interpreter', 'contacted_at', 'phone_number']
    list_filter = ['contacted_at', 'job__date', 'job__status']
    search_fields = ['interpreter__first_name', 'interpreter__last_name', 'job__street_address', 'job__city', 'phone_number']
    date_hierarchy = 'contacted_at'
    ordering = ['-contacted_at']

    readonly_fields = ['job', 'interpreter', 'contacted_at', 'message_sent', 'phone_number']

    fieldsets = (
        ('Contact Details', {
            'fields': ('job', 'interpreter', 'contacted_at', 'phone_number')
        }),
        ('Message', {
            'fields': ('message_sent',)
        }),
    )

    def has_add_permission(self, request):
        # These records are created automatically when messages are sent
        return False

    def has_delete_permission(self, request, obj=None):
        # Keep historical records
        return False
