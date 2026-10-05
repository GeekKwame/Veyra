from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Assessment, Question, AssessmentAttempt
from .serializers import AssessmentLearnerSerializer, SubmitAssessmentSerializer, AssessmentResultSerializer
from apps.roadmaps.models import UserSkillProgress

class AssessmentDetailView(generics.RetrieveAPIView):
    """Retrieve sanitized assessment questions for test-taking."""
    queryset = Assessment.objects.all()
    serializer_class = AssessmentLearnerSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmitAssessmentView(APIView):
    """
    Grades assessment attempt on the server.
    If score >= passing threshold, marks skill as MASTERED and unlocks downstream DAG milestones.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        assessment = get_object_or_404(Assessment, id=pk)
        serializer = SubmitAssessmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_answers = serializer.validated_data['answers']
        questions = list(assessment.questions.all())

        if not questions:
            return Response({'error': 'Assessment has no questions configured.'}, status=status.HTTP_400_BAD_REQUEST)

        correct_count = 0
        for q in questions:
            user_choice = user_answers.get(str(q.id))
            if user_choice and user_choice.strip().upper() == q.correct_answer_id.strip().upper():
                correct_count += 1

        score_pct = round((correct_count / len(questions)) * 100.0, 2)
        is_passed = score_pct >= float(assessment.passing_score_percentage)

        attempt = AssessmentAttempt.objects.create(
            assessment=assessment,
            user=request.user,
            answers=user_answers,
            score_percentage=score_pct,
            is_passed=is_passed
        )

        # If passed, advance learner's skill state in their active roadmap
        if is_passed:
            usp = UserSkillProgress.objects.filter(
                roadmap__user=request.user,
                roadmap__is_active=True,
                skill=assessment.skill
            ).first()
            if usp:
                usp.mark_mastered(score=score_pct)

        return Response(AssessmentResultSerializer(attempt).data, status=status.HTTP_201_CREATED)
