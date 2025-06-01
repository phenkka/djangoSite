from django.contrib import admin
from .models import GeneralStatistics, MainPageInfo, DemandStatistics, GeoStatistics, SkillsStatistics

@admin.register(GeneralStatistics)
class GeneralStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(MainPageInfo)
admin.site.register(DemandStatistics)
admin.site.register(GeoStatistics)
admin.site.register(SkillsStatistics)