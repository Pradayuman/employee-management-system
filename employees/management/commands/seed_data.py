from django.core.management.base import BaseCommand
from faker import Faker
import random
from employees.models import Employee, Department
from attendance.models import Attendance
from performance.models import Performance

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with fake employees, attendance, and performance data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Clear old data
        Attendance.objects.all().delete()
        Performance.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()  # clear departments

        # Create Departments
        department_names = ["HR", "Engineering", "Sales", "Marketing", "Finance"]
        departments = []
        for name in department_names:
            dept, created = Department.objects.get_or_create(name=name)
            departments.append(dept)

        # Create Employees
        employees = []
        for _ in range(30):
            emp = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                date_of_joining=fake.date_between(start_date="-3y", end_date="today"),
                department=random.choice(departments)  # ✅ assign Department instance
            )
            employees.append(emp)

        
        # Attendance Records
        for emp in employees:
            dates = set()  # track used dates
        for _ in range(5):  # 5 attendance records
        # generate a unique date
            while True:
                att_date = fake.date_between(start_date="-3M", end_date="today")
                if att_date not in dates:
                    dates.add(att_date)
                    break

            Attendance.objects.create(
                employee=emp,
                date=att_date,
                status=random.choice(["Present", "Absent", "Late"])
        )


        # Performance Records
        for emp in employees:
            for i in range(2):
                Performance.objects.create(
                    employee=emp,
                    review_date=fake.date_between(start_date="-1y", end_date="today"),
                    rating=random.randint(1, 5),
                    comments=fake.sentence()
                )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
