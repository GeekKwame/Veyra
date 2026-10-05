from django.contrib import admin
from .models import UserRoadmap, UserSkillProgress

class UserSkillProgressInline(admin.TabularInline):
    model = UserSkillProgress
    extra = 0
    fields = ('skill', 'status', 'score_percentage', 'mastered_at')
    readonly_fields = ('skill',)

@admin.register(UserRoadmap)
class UserRoadmapAdmin(admin.ModelAdmin):
    list_display = ('user', 'career', 'committed_hours_per_week', 'projected_completion_date', 'readiness_score', 'is_active')
    list_filter = ('career', 'is_active')
    search_fields = ('user__email', 'career__title')
    inlines = [UserSkillProgressInline]

@admin.register(UserSkillProgress)
class UserSkillProgressAdmin(admin.ModelAdmin):
    list_display = ('roadmap', 'skill', 'status', 'score_percentage', 'mastered_at')
    list_filter = ('status', 'roadmap__career')
    search_fields = ('roadmap__user__email', 'skill__title')
