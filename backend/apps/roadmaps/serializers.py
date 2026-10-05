from rest_framework import serializers
from .models import UserRoadmap, UserSkillProgress
from apps.careers.serializers import SkillSerializer

class UserSkillProgressSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = UserSkillProgress
        fields = ('id', 'skill', 'status', 'score_percentage', 'mastered_at', 'updated_at')

class UserRoadmapSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    career_slug = serializers.CharField(source='career.slug', read_only=True)
    skill_progresses = UserSkillProgressSerializer(many=True, read_only=True)
    progress_summary = serializers.SerializerMethodField()

    class Meta:
        model = UserRoadmap
        fields = (
            'id', 'career', 'career_title', 'career_slug',
            'committed_hours_per_week', 'projected_completion_date',
            'readiness_score', 'is_active', 'started_at',
            'progress_summary', 'skill_progresses'
        )

    def get_progress_summary(self, obj):
        total = obj.skill_progresses.count()
        mastered = obj.skill_progresses.filter(status='MASTERED').count()
        in_progress = obj.skill_progresses.filter(status__in=['IN_PROGRESS', 'PRACTICING', 'ASSESSED']).count()
        available = obj.skill_progresses.filter(status='AVAILABLE').count()
        locked = obj.skill_progresses.filter(status='LOCKED').count()
        return {
            'total': total,
            'mastered': mastered,
            'in_progress': in_progress,
            'available': available,
            'locked': locked,
            'completion_pct': round((mastered / total * 100), 1) if total > 0 else 0.0
        }

class EnrollRoadmapSerializer(serializers.Serializer):
    career_id = serializers.UUIDField()
    committed_hours_per_week = serializers.IntegerField(min_value=1, max_value=60, default=10)

class RecalibrateSerializer(serializers.Serializer):
    hours_per_week = serializers.IntegerField(min_value=1, max_value=60)
