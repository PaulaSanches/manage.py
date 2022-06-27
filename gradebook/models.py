from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Lecturer(models.Model):
    User = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    DOB = models.DateField()


class Class(models.Model):
    Number = models.IntegerField(max_length=100)
    Name = models.CharField(max_length=100)
    Lecturer = models.ForeignKey(Lecturer, null=True, on_delete=models.CASCADE, related_name='lecturerClasses')


class Course(models.Model):
    code = models.IntegerField(max_length=10, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)


class Semester(models.Model):
    currentyear = int(date.today().year)
    year = models.IntegerField(validators=[MinValueValidator(currentyear)], default=currentyear)
    semester = models.CharField(max_length=2, null=False, blank=False)

    def __str__(self):
        return str(self.year) + " " + self.semester

    def get_absolute_url(self):
        return reverse('home')


class Student(models.Model):
    User = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    DOB = models.DateField()


class StudentEnrolment(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Grade = models.IntegerField()
    EnrolTime = models.DateTimeField(auto_now_add=True)
    GradeTime = models.DateTimeField(auto_now=True)
