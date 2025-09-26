from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from django.http import JsonResponse
from performance.models import Performance

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    

def performance_view(request):
    # Example: return all performance records as JSON
    data = list(Performance.objects.values())
    return JsonResponse(data, safe=False)    
