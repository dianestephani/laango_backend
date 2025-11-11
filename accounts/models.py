from django.db import models


class InterpreterProfile(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()

    # Address Information
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, help_text="Two-letter state code (e.g., WA)")
    zip_code = models.CharField(max_length=10)

    # Certification
    dshs_certified = models.BooleanField(default=False, verbose_name="DSHS Certified", help_text="Is this interpreter DSHS certified?")

    # Languages Spoken (in alphabetical order)
    amharic = models.BooleanField(default=False, verbose_name="Amharic")
    farsi = models.BooleanField(default=False, verbose_name="Farsi")
    mandarin = models.BooleanField(default=False, verbose_name="Mandarin")
    portuguese = models.BooleanField(default=False, verbose_name="Portuguese")
    russian = models.BooleanField(default=False, verbose_name="Russian")
    somali = models.BooleanField(default=False, verbose_name="Somali")
    spanish = models.BooleanField(default=False, verbose_name="Spanish")
    tigrinya = models.BooleanField(default=False, verbose_name="Tigrinya")
    vietnamese = models.BooleanField(default=False, verbose_name="Vietnamese")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_languages(self):
        """Return a list of languages this interpreter speaks"""
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
