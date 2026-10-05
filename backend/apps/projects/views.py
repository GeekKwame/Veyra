from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Project, ProjectSubmission
from .serializers import ProjectSerializer, ProjectSubmissionSerializer, CreateSubmissionSerializer

class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

class SubmitProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        serializer = CreateSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = ProjectSubmission.objects.create(
            project=project,
            user=request.user,
            artifact_url=serializer.validated_data['artifact_url'],
            notes=serializer.validated_data.get('notes', ''),
            learner_self_eval=serializer.validated_data.get('learner_self_eval', {}),
            status='SUBMITTED'
        )

        return Response(ProjectSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

class UserSubmissionsView(generics.ListAPIView):
    serializer_class = ProjectSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectSubmission.objects.filter(user=self.request.user)
