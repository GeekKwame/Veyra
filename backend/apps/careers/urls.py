from django.urls import path
from .views import CareerListView, CareerDetailView, DiscoveryEvaluateView

urlpatterns = [
    path('', CareerListView.as_view(), name='career-list'),
    path('discovery/evaluate/', DiscoveryEvaluateView.as_view(), name='discovery-evaluate'),
    path('<slug:slug>/', CareerDetailView.as_view(), name='career-detail'),
]
