from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from attendance.models import Attendance
from django.db.models import Count
from django.utils.timezone import now
from django.http import JsonResponse
from performance.models import Performance


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['department__name', 'date_of_joining']
    search_fields = ['name', 'email']
    ordering_fields = ['date_of_joining']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


def performance_view(request):
    # Example: return all performance records as JSON
    data = list(Performance.objects.values())
    return JsonResponse(data, safe=False)

def charts_view(request):
    # Employees per Department
    departments = Employee.objects.values('department__name').annotate(count=Count('id'))
    department_names = [d['department__name'] for d in departments]
    department_counts = [d['count'] for d in departments]

    # Monthly Attendance (for current year)
    current_year = now().year
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    present_counts = []
    absent_counts = []
    late_counts = []

    for i in range(1,13):
        monthly = Attendance.objects.filter(date__year=current_year, date__month=i)
        present_counts.append(monthly.filter(status='Present').count())
        absent_counts.append(monthly.filter(status='Absent').count())
        late_counts.append(monthly.filter(status='Late').count())

    context = {
        'department_names': department_names,
        'department_counts': department_counts,
        'months': months,
        'present_counts': present_counts,
        'absent_counts': absent_counts,
        'late_counts': late_counts
    }

    return render(request, 'charts.html', context)
