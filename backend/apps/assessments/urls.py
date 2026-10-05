from django.urls import path
from .views import AssessmentDetailView, SubmitAssessmentView

urlpatterns = [
    path('<uuid:pk>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('<uuid:pk>/submit/', SubmitAssessmentView.as_view(), name='assessment-submit'),
]
