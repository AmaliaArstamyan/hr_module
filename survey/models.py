from django.db import models
from django.contrib.auth.models import User

class SurveyForm(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    TYPE_CHOICES = [("text", "Text"), ("choice", "Choice")]
    form = models.ForeignKey(SurveyForm, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    options = models.TextField(blank=True)  # comma-separated

class EmployeeAnswer(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

