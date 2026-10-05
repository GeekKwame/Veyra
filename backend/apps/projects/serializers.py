from rest_framework import serializers
from .models import Project, ProjectSubmission

class ProjectSerializer(serializers.ModelSerializer):
    skill_title = serializers.CharField(source='skill.title', read_only=True)
    career_title = serializers.CharField(source='skill.competency_area.career.title', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'skill', 'skill_title', 'career_title', 'title', 'scenario_brief', 'deliverable_spec', 'rubric_schema', 'is_capstone')

class ProjectSubmissionSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = ProjectSubmission
        fields = ('id', 'project', 'project_title', 'artifact_url', 'notes', 'learner_self_eval', 'ai_feedback', 'final_score', 'status', 'submitted_at')
        read_only_fields = ('ai_feedback', 'final_score', 'status', 'submitted_at')

class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSubmission
        fields = ('artifact_url', 'notes', 'learner_self_eval')
