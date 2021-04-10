from django.contrib import admin

from jobseekerapp.models import Resume, ResumeExperience, ResumeEducation

admin.site.register(Resume)
admin.site.register(ResumeExperience)
admin.site.register(ResumeEducation)
