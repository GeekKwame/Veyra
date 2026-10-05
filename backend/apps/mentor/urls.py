from django.urls import path
from .views import MentorChatView

urlpatterns = [
    path('chat/', MentorChatView.as_view(), name='mentor-chat'),
]
