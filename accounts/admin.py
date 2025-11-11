from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import InterpreterProfile
from jobs.models import Job


class AssignedJobsInline(admin.TabularInline):
    """Inline display of jobs assigned to this interpreter"""
    model = Job
    fk_name = 'assigned_interpreter'
    extra = 0
    can_delete = False
    verbose_name = "Assigned Job"
    verbose_name_plural = "Assigned Jobs (sorted by date, newest first)"
    fields = ['job_link', 'date', 'time', 'job_type', 'status', 'job_location', 'languages_display', 'payment', 'mileage_included']
    readonly_fields = ['job_link', 'date', 'time', 'job_type', 'status', 'job_location', 'languages_display', 'payment', 'mileage_included']

    def has_add_permission(self, request, obj=None):
        return False

    def job_link(self, obj):
        if obj.id:
            url = reverse('admin:jobs_job_change', args=[obj.id])
            languages = obj.get_languages()
            lang_str = ', '.join(languages) if languages else 'No languages'
            return format_html('<a href="{}">{}</a>', url, lang_str)
        return '-'
    job_link.short_description = 'Job Details'

    def job_location(self, obj):
        if obj.id:
            return f"{obj.city}, {obj.state}"
        return '-'
    job_location.short_description = 'Location'

    def languages_display(self, obj):
        if obj.id:
            languages = obj.get_languages()
            return ', '.join(languages) if languages else 'None'
        return '-'
    languages_display.short_description = 'Languages'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-date', '-time')


@admin.register(InterpreterProfile)
class InterpreterProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email_address', 'phone_number', 'city', 'state', 'dshs_certified', 'languages_spoken', 'job_count', 'projected_earnings_display']
    list_filter = ['state', 'dshs_certified', 'spanish', 'russian', 'portuguese', 'mandarin', 'somali', 'farsi', 'vietnamese', 'amharic', 'tigrinya']
    search_fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'city']
    inlines = [AssignedJobsInline]

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
        ('Job Summary', {
            'fields': ('projected_earnings_box',),
        }),
    )

    readonly_fields = ['projected_earnings_box']

    def languages_spoken(self, obj):
        """Display languages spoken in the list view"""
        languages = obj.get_languages()
        return ', '.join(languages) if languages else 'None'
    languages_spoken.short_description = 'Languages'

    def job_count(self, obj):
        """Display number of jobs assigned to this interpreter"""
        return obj.jobs.count()
    job_count.short_description = 'Jobs'

    def projected_earnings_display(self, obj):
        """Display projected earnings from all assigned jobs"""
        if obj.id:
            total = sum(job.payment for job in obj.jobs.all())
            # Format the number first, then pass to format_html
            formatted_amount = '${:,.2f}'.format(total)
            return formatted_amount
        return '-'
    projected_earnings_display.short_description = 'Projected Earnings'

    def projected_earnings_box(self, obj):
        """Display projected earnings box in detail view"""
        if obj.id:
            total = sum(job.payment for job in obj.jobs.all())
            job_count = obj.jobs.count()
            return format_html(
                '<div style="background-color: #d1fae5; border: 2px solid #059669; padding: 15px; border-radius: 8px; text-align: center;">'
                '<strong style="font-size: 14px; color: #065f46;">Projected Earnings</strong><br>'
                '<span style="font-size: 28px; font-weight: bold; color: #047857;">${}</span><br>'
                '<span style="font-size: 12px; color: #047857;">from {} job{}</span>'
                '</div>',
                '{:,.2f}'.format(total),
                job_count,
                '' if job_count == 1 else 's'
            )
        return '-'
    projected_earnings_box.short_description = 'Projected Earnings'
