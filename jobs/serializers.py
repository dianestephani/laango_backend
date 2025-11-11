from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()
    assigned_interpreter_name = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id',
            'languages',
            'street_address',
            'city',
            'state',
            'zip_code',
            'full_address',
            'date',
            'time',
            'job_type',
            'status',
            'requires_dshs_certification',
            'payment',
            'mileage_included',
            'assigned_interpreter',
            'assigned_interpreter_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_languages(self, obj):
        return obj.get_languages()

    def get_full_address(self, obj):
        return f"{obj.street_address}, {obj.city}, {obj.state} {obj.zip_code}"

    def get_assigned_interpreter_name(self, obj):
        if obj.assigned_interpreter:
            return f"{obj.assigned_interpreter.first_name} {obj.assigned_interpreter.last_name}"
        return None
