from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Performance
from .serializers import PerformanceSerializer

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
