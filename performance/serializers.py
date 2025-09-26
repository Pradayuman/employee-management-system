from rest_framework import serializers
from .models import Performance

class PerformanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Performance
        fields = ['id', 'employee', 'employee_name', 'rating', 'review_date', 'comments']
