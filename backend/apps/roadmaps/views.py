from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import UserRoadmap, UserSkillProgress
from apps.careers.models import Career, Skill
from .serializers import UserRoadmapSerializer, EnrollRoadmapSerializer, RecalibrateSerializer
from .engine.pacing import recalibrate_schedule

class ActiveRoadmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        roadmap = UserRoadmap.objects.filter(user=request.user, is_active=True).first()
        if not roadmap:
            return Response({'detail': 'No active roadmap found. Please enroll in a career track.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRoadmapSerializer(roadmap)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EnrollRoadmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = EnrollRoadmapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        career = get_object_or_404(Career, id=serializer.validated_data['career_id'])
        hours_per_week = serializer.validated_data['committed_hours_per_week']

        # Deactivate any previous active roadmaps
        UserRoadmap.objects.filter(user=request.user, is_active=True).update(is_active=False)

        roadmap, created = UserRoadmap.objects.get_or_create(
            user=request.user,
            career=career,
            defaults={
                'committed_hours_per_week': hours_per_week,
                'is_active': True,
            }
        )
        if not created:
            roadmap.is_active = True
            roadmap.committed_hours_per_week = hours_per_week
            roadmap.save()

        roadmap.initialize_progress()
        recalibrate_schedule(roadmap, hours_per_week)

        return Response(UserRoadmapSerializer(roadmap).data, status=status.HTTP_201_CREATED)

class RecalibratePacingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = RecalibrateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        roadmap = get_object_or_404(UserRoadmap, user=request.user, is_active=True)
        recalibrate_schedule(roadmap, serializer.validated_data['hours_per_week'])

        return Response({
            'detail': 'Roadmap timeline recalibrated successfully.',
            'committed_hours_per_week': roadmap.committed_hours_per_week,
            'projected_completion_date': roadmap.projected_completion_date
        }, status=status.HTTP_200_OK)

class UpdateSkillStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, skill_id):
        target_status = request.data.get('status')
        if target_status not in ['IN_PROGRESS', 'PRACTICING']:
            return Response({'error': 'Invalid status transition.'}, status=status.HTTP_400_BAD_REQUEST)

        usp = get_object_or_404(
            UserSkillProgress,
            roadmap__user=request.user,
            roadmap__is_active=True,
            skill_id=skill_id
        )

        if usp.status == 'LOCKED':
            return Response({'error': 'Cannot start a locked skill. Incomplete prerequisites.'}, status=status.HTTP_403_FORBIDDEN)

        usp.status = target_status
        usp.save(update_fields=['status', 'updated_at'])

        return Response({'status': usp.status, 'skill_id': str(skill_id)}, status=status.HTTP_200_OK)
