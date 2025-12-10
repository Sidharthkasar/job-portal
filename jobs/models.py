from django.db import models

from django.db import models

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full-time')

    def __str__(self):
        return self.title
