from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from employees.models import Employee, Department
from performance.models import Performance
from rest_framework.authtoken.models import Token

class PerformanceAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name="Sales")
        self.employee = Employee.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            phone="9876543210",
            address="456 Park Ave",
            date_of_joining="2023-01-01",
            department=self.department
        )

        # Token auth if applicable
        self.token = Token.objects.create(user=self.employee.user) if hasattr(self.employee, 'user') else None
        if self.token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create performance record
        self.performance = Performance.objects.create(
            employee=self.employee,
            review_date="2025-09-25",
            rating=4,
            comments="Good performance"
        )

    def test_list_performance(self):
        url = reverse('performance-list')  # Make sure your router has 'performance' basename
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 4)

    def test_create_performance(self):
        url = reverse('performance-list')
        data = {
            "employee": self.employee.id,
            "review_date": "2025-09-26",
            "rating": 5,
            "comments": "Excellent"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 2)
