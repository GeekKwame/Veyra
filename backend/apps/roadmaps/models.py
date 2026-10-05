import uuid
from django.db import models
from django.conf import settings
from apps.careers.models import Career, Skill

class UserRoadmap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmaps')
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, related_name='enrollments')
    committed_hours_per_week = models.PositiveIntegerField(default=10)
    projected_completion_date = models.DateField(null=True, blank=True)
    readiness_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'career')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.email} → {self.career.title} ({self.readiness_score}%)"

    def initialize_progress(self):
        """
        Creates UserSkillProgress records for all skills in the career.
        Unlocks root skills (those with 0 prerequisites).
        """
        skills = Skill.objects.filter(competency_area__career=self.career)
        created_records = []

        for skill in skills:
            prereqs_count = skill.downstream_links.count()
            initial_status = 'AVAILABLE' if prereqs_count == 0 else 'LOCKED'
            usp, _ = UserSkillProgress.objects.get_or_create(
                roadmap=self,
                skill=skill,
                defaults={'status': initial_status}
            )
            created_records.append(usp)

        return created_records

    def check_and_unlock_downstream(self, mastered_skill: Skill):
        """
        When a skill is mastered, inspect all downstream skills that depend on it.
        If all strict prerequisites are mastered, unlock the downstream skill.
        """
        downstream_links = mastered_skill.prerequisite_links.filter(is_strict=True)
        for link in downstream_links:
            target_skill = link.skill
            usp = UserSkillProgress.objects.filter(roadmap=self, skill=target_skill).first()
            if usp and usp.status == 'LOCKED':
                # Check if all strict prerequisites of target_skill are MASTERED
                prereq_ids = target_skill.downstream_links.filter(is_strict=True).values_list('prerequisite_skill_id', flat=True)
                unmastered = UserSkillProgress.objects.filter(
                    roadmap=self,
                    skill_id__in=prereq_ids
                ).exclude(status='MASTERED').exists()

                if not unmastered:
                    usp.status = 'AVAILABLE'
                    usp.save(update_fields=['status', 'updated_at'])

class UserSkillProgress(models.Model):
    STATUS_CHOICES = [
        ('LOCKED', 'Locked (Prerequisites Incomplete)'),
        ('AVAILABLE', 'Available to Start'),
        ('IN_PROGRESS', 'In Progress (Studying)'),
        ('PRACTICING', 'Practicing (Drills / Projects)'),
        ('ASSESSED', 'Assessed (Evaluation Complete)'),
        ('MASTERED', 'Mastered & Verified'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roadmap = models.ForeignKey(UserRoadmap, on_delete=models.CASCADE, related_name='skill_progresses')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_progresses')
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default='LOCKED')
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mastered_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('roadmap', 'skill')
        ordering = ['skill__title']

    def __str__(self):
        return f"{self.roadmap.user.email}: {self.skill.title} [{self.status}]"

    def mark_mastered(self, score: float = 100.0):
        from django.utils import timezone
        self.status = 'MASTERED'
        self.score_percentage = score
        self.mastered_at = timezone.now()
        self.save(update_fields=['status', 'score_percentage', 'mastered_at', 'updated_at'])
        self.roadmap.check_and_unlock_downstream(self.skill)
