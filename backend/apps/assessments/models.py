import uuid
from django.db import models
from django.conf import settings
from apps.careers.models import Skill

class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=255)
    passing_score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    time_limit_minutes = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.skill.title})"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Single Answer'),
        ('SCENARIO', 'Situational Case-Study Judgment'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField()
    question_type = models.CharField(max_length=32, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    options = models.JSONField(help_text="List of choices: [{'id': 'A', 'text': '...'}, ...]")
    correct_answer_id = models.CharField(max_length=16, help_text="ID of correct option (e.g. 'A')")
    explanation = models.TextField(help_text="Pedagogical explanation shown upon completion.")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"Q: {self.prompt[:60]}..."

class AssessmentAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_attempts')
    answers = models.JSONField(help_text="User selected answers: {'question_id': 'selected_id'}")
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_passed = models.BooleanField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        result = "PASSED" if self.is_passed else "FAILED"
        return f"{self.user.email} → {self.assessment.title}: {self.score_percentage}% [{result}]"
