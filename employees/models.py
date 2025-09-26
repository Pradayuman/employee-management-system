from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_joining = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
