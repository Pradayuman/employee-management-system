from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from employees.models import Department, Employee
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase, Client
from django.urls import reverse
from employees.models import Employee, Department
from attendance.models import Attendance
from performance.models import Performance
from django.utils.timezone import now

class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a department
        self.department = Department.objects.create(name='IT')

        # Create an employee
        self.employee = Employee.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St',
            date_of_joining='2023-01-01',
            department=self.department
        )

    def test_list_employees(self):
        url = reverse('employee-list')  # ViewSet default route: 'employee-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_employee(self):
        url = reverse('employee-list')
        data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "0987654321",
            "address": "456 Another St",
            "date_of_joining": "2023-05-01",
            "department_id": self.department.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_update_employee(self):
        url = reverse('employee-detail', args=[self.employee.id])
        data = {"name": "John Updated"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "John Updated")

    def test_delete_employee(self):
        url = reverse('employee-detail', args=[self.employee.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
        
class DepartmentAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='deptuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.department = Department.objects.create(name='HR')

    def test_list_departments(self):
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_department(self):
        url = reverse('department-list')
        data = {"name": "Finance"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)
        



class EmployeeViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # Create Department
        self.department = Department.objects.create(name="Engineering")

        # Create Employees
        self.employee1 = Employee.objects.create(
            name="Alice",
            email="alice@example.com",
            phone="1111111111",
            address="123 Street",
            date_of_joining="2023-01-01",
            department=self.department
        )
        self.employee2 = Employee.objects.create(
            name="Bob",
            email="bob@example.com",
            phone="2222222222",
            address="456 Avenue",
            date_of_joining="2023-02-01",
            department=self.department
        )

        # Create Attendance
        Attendance.objects.create(
            employee=self.employee1,
            date=now().date(),
            status="Present"
        )
        Attendance.objects.create(
            employee=self.employee2,
            date=now().date(),
            status="Absent"
        )

        # Create Performance
        Performance.objects.create(
            employee=self.employee1,
            review_date=now().date(),
            rating=5,
            comments="Excellent"
        )
        Performance.objects.create(
            employee=self.employee2,
            review_date=now().date(),
            rating=3,
            comments="Average"
        )

    def test_charts_view(self):
        """Test that charts_view returns 200 and correct context."""
        response = self.client.get(reverse('charts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('department_names', response.context)
        self.assertIn('department_counts', response.context)
        self.assertIn('months', response.context)
        self.assertIn('present_counts', response.context)
        self.assertIn('absent_counts', response.context)
        self.assertIn('late_counts', response.context)
        # Check counts
        self.assertEqual(response.context['department_counts'][0], 2)

    def test_performance_view_json(self):
        """Test that performance_view returns all performance records as JSON."""
        response = self.client.get(reverse('performance'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        ratings = [record['rating'] for record in response.json()]
        self.assertIn(5, ratings)
        self.assertIn(3, ratings)
