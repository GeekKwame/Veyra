from django.contrib import admin
from .models import Assessment, Question, AssessmentAttempt

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'passing_score_percentage', 'time_limit_minutes')
    list_filter = ('skill__competency_area__career',)
    search_fields = ('title', 'skill__title')
    inlines = [QuestionInline]

@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'score_percentage', 'is_passed', 'completed_at')
    list_filter = ('is_passed', 'assessment__skill__competency_area__career')
    search_fields = ('user__email', 'assessment__title')
