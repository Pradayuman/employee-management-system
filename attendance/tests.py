from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from employees.models import Employee, Department
from attendance.models import Attendance
from rest_framework.authtoken.models import Token

class AttendanceAPITestCase(APITestCase):

    def setUp(self):
        # Create department and employee
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = Department.objects.create(name="Engineering")
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            date_of_joining="2022-01-01",
            department=self.department
        )

        # Create token
        self.token = Token.objects.create(user=self.employee.user) if hasattr(self.employee, 'user') else None
        if self.token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create an attendance record
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            date="2025-09-26",
            status="Present"
        )

    def test_list_attendance(self):
        url = reverse('attendance-list')  # Make sure your router has 'attendance' basename
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'Present')

    def test_create_attendance(self):
        url = reverse('attendance-list')
        data = {
            "employee": self.employee.id,
            "date": "2025-09-27",
            "status": "Absent"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)
