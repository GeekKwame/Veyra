import uuid
from django.db import models
from django.conf import settings
from apps.careers.models import Skill

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    scenario_brief = models.TextField(help_text="Authentic, real-world workplace scenario.")
    deliverable_spec = models.TextField(help_text="Explicit output requirements (e.g. GitHub URL, PDF spreadsheet).")
    rubric_schema = models.JSONField(
        default=list,
        help_text="List of evaluation criteria with weights and 1-4 descriptive anchors."
    )
    is_capstone = models.BooleanField(default=False, help_text="Capstone projects are hard gates for career readiness.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        prefix = "[CAPSTONE] " if self.is_capstone else ""
        return f"{prefix}{self.title} ({self.skill.title})"

class ProjectSubmission(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted for Review'),
        ('EVALUATED', 'Evaluated (Feedback Ready)'),
        ('NEEDS_REVISION', 'Needs Revision'),
        ('APPROVED', 'Approved / Mastered'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_submissions')
    artifact_url = models.URLField(max_length=1024, help_text="Public URL to deliverable (GitHub, Google Docs, Figma, R2 storage).")
    notes = models.TextField(blank=True, help_text="Student reflections or execution notes.")
    learner_self_eval = models.JSONField(default=dict, blank=True)
    ai_feedback = models.JSONField(default=dict, blank=True)
    final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='SUBMITTED')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.email} → {self.project.title} [{self.status}]"
