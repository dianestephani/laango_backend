from django.db import models


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('legal', 'Legal'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    language = models.CharField(max_length=100)
    location = models.CharField(max_length=255, help_text="Address of the job location")
    date = models.DateField()
    time = models.TimeField()
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='medical')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unassigned')
    requires_dshs_certification = models.BooleanField(default=False, help_text="Does this job require DSHS certification?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.language} - {self.job_type} on {self.date} at {self.time}"
