from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import AIMentorService

class MentorChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        skill_id = request.data.get('skill_id')

        if not user_message:
            return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = AIMentorService.generate_response(
            user=request.user,
            user_message=user_message,
            skill_id=skill_id
        )

        return Response(response_data, status=status.HTTP_200_OK)
