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

    # Languages Needed (in alphabetical order)
    amharic = models.BooleanField(default=False, verbose_name="Amharic")
    farsi = models.BooleanField(default=False, verbose_name="Farsi")
    mandarin = models.BooleanField(default=False, verbose_name="Mandarin")
    portuguese = models.BooleanField(default=False, verbose_name="Portuguese")
    russian = models.BooleanField(default=False, verbose_name="Russian")
    somali = models.BooleanField(default=False, verbose_name="Somali")
    spanish = models.BooleanField(default=False, verbose_name="Spanish")
    tigrinya = models.BooleanField(default=False, verbose_name="Tigrinya")
    vietnamese = models.BooleanField(default=False, verbose_name="Vietnamese")

    # Job Location
    street_address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=2, default='', help_text="Two-letter state code (e.g., WA)")
    zip_code = models.CharField(max_length=10, default='')

    # Job Details
    date = models.DateField()
    time = models.TimeField()
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='medical')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unassigned')
    requires_dshs_certification = models.BooleanField(default=False, help_text="Does this job require DSHS certification?")

    # Payment Details
    payment = models.IntegerField(default=0, help_text="Payment amount for this job")
    mileage_included = models.BooleanField(default=False, help_text="Can mileage be included for this job?")

    # Assigned Interpreter
    assigned_interpreter = models.ForeignKey(
        'accounts.InterpreterProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs',
        help_text="The interpreter assigned to this job"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        languages = self.get_languages()
        lang_str = ', '.join(languages) if languages else 'No languages'
        return f"{lang_str} - {self.job_type} on {self.date} at {self.time}"

    def get_languages(self):
        """Return a list of languages needed for this job"""
        languages = []
        if self.amharic:
            languages.append('Amharic')
        if self.farsi:
            languages.append('Farsi')
        if self.mandarin:
            languages.append('Mandarin')
        if self.portuguese:
            languages.append('Portuguese')
        if self.russian:
            languages.append('Russian')
        if self.somali:
            languages.append('Somali')
        if self.spanish:
            languages.append('Spanish')
        if self.tigrinya:
            languages.append('Tigrinya')
        if self.vietnamese:
            languages.append('Vietnamese')
        return languages
