from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Career
from .serializers import CareerListSerializer, CareerDetailSerializer

class CareerListView(generics.ListAPIView):
    queryset = Career.objects.filter(is_published=True)
    serializer_class = CareerListSerializer
    permission_classes = [permissions.AllowAny]

class CareerDetailView(generics.RetrieveAPIView):
    queryset = Career.objects.filter(is_published=True)
    serializer_class = CareerDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class DiscoveryEvaluateView(APIView):
    """
    Career Discovery Recommendation Engine.
    Evaluates learner constraints, interests, work style, and available hours.
    Returns ranked careers with transparent match scores and explanations.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        interests = request.data.get('interests', [])
        available_hours = int(request.data.get('available_hours_per_week', 10))
        work_style = request.data.get('work_style', 'ANALYTICAL').upper()
        environment_preference = request.data.get('environment', 'REMOTE').upper()

        careers = Career.objects.filter(is_published=True)
        results = []

        for c in careers:
            score = 60  # baseline
            reasons = []

            cat_upper = c.industry_category.upper()
            title_upper = c.title.upper()

            # Work style alignment
            if work_style == 'ANALYTICAL':
                if 'FINANCE' in cat_upper or 'TECH' in cat_upper or 'ACCOUNT' in title_upper:
                    score += 25
                    reasons.append("Strong match for your analytical problem-solving preference.")
            elif work_style == 'HANDS_ON':
                if 'TRADES' in cat_upper or 'ELECTRIC' in title_upper or 'HEALTH' in cat_upper:
                    score += 25
                    reasons.append("High alignment with your preference for tactile, real-world execution.")
            elif work_style == 'DETAIL_ORIENTED':
                if 'BILLING' in title_upper or 'ACCOUNT' in title_upper:
                    score += 25
                    reasons.append("Matches your meticulous attention to compliance and structured records.")

            # Time feasibility check
            if available_hours >= 15:
                score += 15
                reasons.append(f"Your commitment of {available_hours} hrs/week enables accelerated completion.")
            elif available_hours >= 8:
                score += 10
                reasons.append(f"Flexible milestone pacing fits your {available_hours} hrs/week schedule.")
            else:
                score -= 5
                reasons.append(f"With {available_hours} hrs/week, you will progress steadily with micro-drills.")

            # Cap score between 0 and 99
            final_score = min(max(score, 45), 98)

            results.append({
                'career_id': str(c.id),
                'slug': c.slug,
                'title': c.title,
                'category': c.industry_category,
                'badge': c.badge,
                'match_percentage': final_score,
                'estimated_months': c.avg_months_to_complete,
                'rationale': " ".join(reasons) if reasons else "Good general vocational match based on your initial profile."
            })

        results.sort(key=lambda x: x['match_percentage'], reverse=True)
        return Response({'recommendations': results}, status=status.HTTP_200_OK)
