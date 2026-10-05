from django.contrib import admin
from .models import Project, ProjectSubmission

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'is_capstone', 'created_at')
    list_filter = ('is_capstone', 'skill__competency_area__career')
    search_fields = ('title', 'scenario_brief', 'skill__title')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'status', 'final_score', 'submitted_at')
    list_filter = ('status', 'project__is_capstone')
    search_fields = ('user__email', 'project__title', 'artifact_url')
    actions = ['approve_submission']

    @admin.action(description="Approve selected submissions")
    def approve_submission(self, request, queryset):
        queryset.update(status='APPROVED', final_score=100.0)
