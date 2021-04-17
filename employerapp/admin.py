from django.contrib import admin

from employerapp.models import Vacancy, SendOffers, Favorites


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('vacancy_name', 'employer', 'action',)
    list_filter = ('action', )


admin.site.register(SendOffers)
admin.site.register(Favorites)


