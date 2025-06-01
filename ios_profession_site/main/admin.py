from django.contrib import admin
from .models import GeneralStatistics, MainPageInfo

@admin.register(GeneralStatistics)
class GeneralStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(MainPageInfo)