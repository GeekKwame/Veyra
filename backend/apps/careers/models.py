import uuid
from django.db import models
from django.core.exceptions import ValidationError
from .engine.dag import DirectedAcyclicGraph, CyclicDependencyError

class Career(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=128, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry_category = models.CharField(max_length=128)
    avg_months_to_complete = models.PositiveIntegerField(default=6)
    badge = models.CharField(max_length=64, blank=True, default='High Demand')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['industry_category', 'title']

    def __str__(self):
        return f"{self.title} ({self.industry_category})"

    def build_dag(self) -> DirectedAcyclicGraph:
        """Constructs and returns the full DAG for all skills in this career."""
        dag = DirectedAcyclicGraph()
        skills = Skill.objects.filter(competency_area__career=self).values_list('id', flat=True)
        for s_id in skills:
            dag.add_node(str(s_id))

        prereqs = SkillPrerequisite.objects.filter(skill__competency_area__career=self).values_list(
            'prerequisite_skill_id', 'skill_id'
        )
        for prereq_id, skill_id in prereqs:
            dag.add_edge(str(prereq_id), str(skill_id))

        return dag

class CompetencyArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='competencies')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return f"{self.career.title} → {self.title}"

class Skill(models.Model):
    TAXONOMY_CHOICES = [
        ('REMEMBER', 'Remember'),
        ('UNDERSTAND', 'Understand'),
        ('APPLY', 'Apply'),
        ('ANALYZE', 'Analyze'),
        ('EVALUATE', 'Evaluate'),
        ('CREATE', 'Create'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competency_area = models.ForeignKey(CompetencyArea, on_delete=models.CASCADE, related_name='skills')
    slug = models.SlugField(max_length=128)
    title = models.CharField(max_length=255)
    description = models.TextField()
    taxonomy = models.CharField(max_length=16, choices=TAXONOMY_CHOICES, default='APPLY')
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('competency_area', 'slug')
        ordering = ['title']

    def __str__(self):
        return f"{self.title} [{self.taxonomy}]"

    def get_prerequisites(self):
        """Returns direct prerequisite skills."""
        return Skill.objects.filter(downstream_links__skill=self)

class SkillPrerequisite(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='prerequisite_links')
    prerequisite_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='downstream_links')
    is_strict = models.BooleanField(default=True, help_text="Strict blockers must be completed before unlocking downstream skill.")

    class Meta:
        unique_together = ('skill', 'prerequisite_skill')

    def __str__(self):
        return f"{self.prerequisite_skill.title} ──▶ {self.skill.title}"

    def clean(self):
        if self.skill_id == self.prerequisite_skill_id:
            raise ValidationError("A skill cannot be a prerequisite of itself.")

        # Ensure both skills belong to the same career
        if self.skill.competency_area.career_id != self.prerequisite_skill.competency_area.career_id:
            raise ValidationError("Prerequisites must belong to the same career track.")

        # Cycle check validation
        dag = self.skill.competency_area.career.build_dag()
        try:
            dag.add_edge(str(self.prerequisite_skill_id), str(self.skill_id))
            if dag.detect_cycle():
                raise ValidationError("Adding this prerequisite would create a circular dependency cycle.")
        except CyclicDependencyError as e:
            raise ValidationError(str(e))

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return f"{self.skill.title} → {self.title}"

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('VIDEO', 'Video / Lecture'),
        ('ARTICLE', 'Article / Guide'),
        ('DOCUMENTATION', 'Official Documentation'),
        ('BOOK', 'Legally Free Book / Text'),
        ('INTERACTIVE_LAB', 'Interactive Practice / Lab'),
        ('SIMULATION', 'Simulation / Sandbox'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('VALIDATING', 'Validating'),
        ('IN_REVIEW', 'In Review'),
        ('PUBLISHED', 'Published'),
        ('DEGRADED', 'Degraded / Broken'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=1024)
    provider_name = models.CharField(max_length=128)
    resource_type = models.CharField(max_length=32, choices=RESOURCE_TYPE_CHOICES)
    estimated_minutes = models.PositiveIntegerField(default=15)
    is_completely_free = models.BooleanField(default=True)
    verification_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='DRAFT')
    last_verified_at = models.DateTimeField(null=True, blank=True)
    http_status_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-verification_status', 'title']

    def __str__(self):
        return f"[{self.verification_status}] {self.title} ({self.provider_name})"
