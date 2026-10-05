from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/careers/', include('apps.careers.urls')),
    path('api/v1/roadmaps/', include('apps.roadmaps.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/assessments/', include('apps.assessments.urls')),
    path('api/v1/mentor/', include('apps.mentor.urls')),
]
