from django.urls import path
from .views import ProjectDetailView, SubmitProjectView, UserSubmissionsView

urlpatterns = [
    path('submissions/', UserSubmissionsView.as_view(), name='user-submissions'),
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<uuid:project_id>/submit/', SubmitProjectView.as_view(), name='project-submit'),
]
