from django.contrib import admin
from django.contrib.admin import StackedInline

from jobseekerapp.models import Resume, ResumeExperience, ResumeEducation


def name(obj):
    return f'{obj.user.user.first_name} {obj.user.user.last_name} {obj.user.middle_name}'


class ResumeExperienceInline(StackedInline):
    model = ResumeExperience
    exclude = ('is_active',)
    extra = 0


class ResumeEducationInline(StackedInline):
    model = ResumeEducation
    exclude = ('is_active',)
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (name, 'name', 'status')
    list_filter = ('status', )
    inlines = [ResumeEducationInline, ResumeExperienceInline]
    fieldsets = (
        ('Раздел модерации', {
            'fields': ('status', 'failed_moderation')
        }),
        ('Общая информация', {
            'fields': ('user', 'name', ('salary_min', 'salary_max', 'currency'),
                        'key_skills', 'about', 'is_active')

        })
    )


# admin.site.register(ResumeExperience)
# admin.site.register(ResumeEducation)
