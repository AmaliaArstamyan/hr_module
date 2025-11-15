from django.contrib import admin
from .models import SurveyForm, Question, EmployeeAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(SurveyForm)
class SurveyFormAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "form", "type")

@admin.register(EmployeeAnswer)
class EmployeeAnswerAdmin(admin.ModelAdmin):
    list_display = ("employee", "question", "answer", "submitted_at")
