from django.urls import path
from .views import ActiveRoadmapView, EnrollRoadmapView, RecalibratePacingView, UpdateSkillStatusView

urlpatterns = [
    path('active/', ActiveRoadmapView.as_view(), name='roadmap-active'),
    path('enroll/', EnrollRoadmapView.as_view(), name='roadmap-enroll'),
    path('recalibrate/', RecalibratePacingView.as_view(), name='roadmap-recalibrate'),
    path('skills/<uuid:skill_id>/status/', UpdateSkillStatusView.as_view(), name='skill-status-update'),
]
