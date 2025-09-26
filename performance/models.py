from django.db import models
from employees.models import Employee

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5
    review_date = models.DateField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.rating}"
