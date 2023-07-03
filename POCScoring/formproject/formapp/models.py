from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for employee information as necessary


class Form(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    assigned_employees = models.ManyToManyField(Employee, through='FormAssignment')
    is_draft = models.BooleanField(default=False)  # New field

    
class Section(models.Model):
    title = models.CharField(max_length=200)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    order = models.IntegerField()  # For ordering the sections

class Subsection(models.Model):
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    order = models.IntegerField()  # For ordering the subsections within a section


class Question(models.Model):
    text = models.CharField(max_length=200)
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, null=True)
    order = models.IntegerField()  # For ordering the questions within a subsection

class Response(models.Model):
    assignment = models.ForeignKey('FormAssignment', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    score = models.IntegerField(null=True, blank=True)  # New field to hold the score, allowing null or blank values

class FormAssignment(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    responses = models.ManyToManyField(Response)  # Add this line
    completed = models.BooleanField(default=False)
