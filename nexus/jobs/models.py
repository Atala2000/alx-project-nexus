from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    company = models.CharField(max_length=200, db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['company']),
        ]

    def __str__(self):
        return self.title


class Location(models.Model):
    job = models.ForeignKey(Job, related_name='locations', on_delete=models.CASCADE, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['city', 'country']),
        ]


class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE, db_index=True)
    applicant_name = models.CharField(max_length=200, db_index=True)
    applicant_email = models.EmailField(db_index=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)

    applied_by = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"

    class Meta:
        indexes = [
            models.Index(fields=['applicant_email']),
        ]


class JobPosting(models.Model):
    job = models.ForeignKey(Job, related_name='job_postings', on_delete=models.CASCADE, db_index=True)
    posted_date = models.DateTimeField(auto_now_add=True, db_index=True)
    closing_date = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['posted_date']),
            models.Index(fields=['closing_date']),
        ]

    def __str__(self):
        return f"{self.job.title} - Posted on {self.posted_date.strftime('%Y-%m-%d')}"
