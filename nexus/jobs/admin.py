from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Job, Location, Application, JobPosting


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'salary', 'posted_by')
    search_fields = ('title', 'company', 'description')
    list_filter = ('company',)
    ordering = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('job', 'city', 'country')
    search_fields = ('city', 'country')
    list_filter = ('city', 'country')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant_name', 'applicant_email', 'applied_by')
    search_fields = ('applicant_name', 'applicant_email')
    list_filter = ('job',)


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('job', 'posted_date', 'closing_date')
    search_fields = ('job__title',)
    list_filter = ('posted_date', 'closing_date')
