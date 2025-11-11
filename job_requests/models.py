from django.db import models
from jobs.models import Job
from accounts.models import InterpreterProfile


class InterpreterContact(models.Model):
    """
    Tracks each time an interpreter is contacted for a job
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='interpreter_contacts')
    interpreter = models.ForeignKey(InterpreterProfile, on_delete=models.CASCADE, related_name='job_contacts')
    contacted_at = models.DateTimeField(auto_now_add=True)
    message_sent = models.TextField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Interpreter Contact"
        verbose_name_plural = "Interpreter Contacts"
        ordering = ['-contacted_at']

    def __str__(self):
        return f"{self.interpreter} contacted for {self.job} on {self.contacted_at.strftime('%m/%d/%Y %I:%M %p')}"
