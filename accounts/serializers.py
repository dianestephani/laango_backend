from rest_framework import serializers
from .models import InterpreterProfile
from jobs.serializers import JobSerializer


class InterpreterProfileSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    assigned_jobs = JobSerializer(source='jobs', many=True, read_only=True)
    job_count = serializers.SerializerMethodField()

    class Meta:
        model = InterpreterProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'email_address',
            'street_address',
            'city',
            'state',
            'zip_code',
            'dshs_certified',
            'languages',
            'assigned_jobs',
            'job_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_languages(self, obj):
        return obj.get_languages()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_job_count(self, obj):
        return obj.jobs.count()
