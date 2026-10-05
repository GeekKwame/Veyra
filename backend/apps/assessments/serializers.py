from rest_framework import serializers
from .models import Assessment, Question, AssessmentAttempt

class QuestionLearnerSerializer(serializers.ModelSerializer):
    """Sanitized questions for active test-taking (no answers/explanations exposed)."""
    class Meta:
        model = Question
        fields = ('id', 'prompt', 'question_type', 'options', 'sort_order')

class AssessmentLearnerSerializer(serializers.ModelSerializer):
    questions = QuestionLearnerSerializer(many=True, read_only=True)
    skill_title = serializers.CharField(source='skill.title', read_only=True)

    class Meta:
        model = Assessment
        fields = ('id', 'skill', 'skill_title', 'title', 'passing_score_percentage', 'time_limit_minutes', 'questions')

class SubmitAssessmentSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.CharField(), help_text="{'question_id': 'option_id'}")

class AssessmentResultSerializer(serializers.ModelSerializer):
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    remediation = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentAttempt
        fields = ('id', 'assessment', 'assessment_title', 'score_percentage', 'is_passed', 'completed_at', 'remediation')

    def get_remediation(self, obj):
        # Build remediation items for incorrect questions
        remediation_items = []
        for q in obj.assessment.questions.all():
            user_choice = obj.answers.get(str(q.id))
            is_correct = (user_choice == q.correct_answer_id)
            remediation_items.append({
                'question_id': str(q.id),
                'prompt': q.prompt,
                'user_choice': user_choice,
                'correct_choice': q.correct_answer_id,
                'is_correct': is_correct,
                'explanation': q.explanation
            })
        return remediation_items
