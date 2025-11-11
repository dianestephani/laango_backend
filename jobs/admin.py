from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['language', 'job_type', 'date', 'time', 'location', 'status', 'requires_dshs_certification', 'created_at']
    list_filter = ['status', 'job_type', 'date', 'requires_dshs_certification']
    search_fields = ['language', 'location']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']
