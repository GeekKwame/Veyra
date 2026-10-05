from rest_framework import serializers
from .models import Career, CompetencyArea, Skill, SkillPrerequisite, Topic, Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'title', 'url', 'provider_name', 'resource_type', 'estimated_minutes', 'is_completely_free', 'verification_status')

class TopicSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'sort_order', 'resources')

class SkillSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    prerequisites = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ('id', 'slug', 'title', 'description', 'taxonomy', 'estimated_hours', 'prerequisites', 'topics')

    def get_prerequisites(self, obj):
        return [str(p.prerequisite_skill_id) for p in obj.prerequisite_links.all()]

class CompetencyAreaSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = CompetencyArea
        fields = ('id', 'title', 'description', 'sort_order', 'skills')

class CareerListSerializer(serializers.ModelSerializer):
    total_skills = serializers.SerializerMethodField()
    total_estimated_hours = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ('id', 'slug', 'title', 'description', 'industry_category', 'avg_months_to_complete', 'badge', 'total_skills', 'total_estimated_hours')

    def get_total_skills(self, obj):
        return Skill.objects.filter(competency_area__career=obj).count()

    def get_total_estimated_hours(self, obj):
        from django.db.models import Sum
        total = Skill.objects.filter(competency_area__career=obj).aggregate(Sum('estimated_hours'))['estimated_hours__sum']
        return float(total or 0.0)

class CareerDetailSerializer(serializers.ModelSerializer):
    competencies = CompetencyAreaSerializer(many=True, read_only=True)
    milestones = serializers.SerializerMethodField()

    class Meta:
        model = Career
        fields = ('id', 'slug', 'title', 'description', 'industry_category', 'avg_months_to_complete', 'badge', 'competencies', 'milestones')

    def get_milestones(self, obj):
        dag = obj.build_dag()
        try:
            return dag.resolve_milestone_levels()
        except Exception:
            return []
