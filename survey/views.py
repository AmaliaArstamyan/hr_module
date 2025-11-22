# survey/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import SurveyForm, Question, EmployeeAnswer
import json
from django.contrib import messages

# ------------------------
# Redirect after login
# ------------------------


@login_required
def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='HR').exists():
        return redirect('survey:home')
    elif user.groups.filter(name='TeamLead').exists():
        return redirect('survey:home')
    elif user.groups.filter(name='Employee').exists():
        return redirect('survey:home')
    else:
        messages.error(request, "Your account is not assigned to any role. Contact admin.")
        return redirect('login')



def custom_login(request):
    return render(request, 'login.html', {})

# ------------------------
# User Registration
# ------------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            # Назначаем группу
            role = form.cleaned_data.get('role')
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            # Авто-логин
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user:
                login(request, user)

            return redirect('redirect_after_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



# ------------------------
# Dashboards
# ------------------------
@login_required
def hr_dashboard(request):
    answers = EmployeeAnswer.objects.select_related('employee', 'question').all()
    return render(request, "survey/hr_dashboard.html", {"answers": answers})

@login_required
def teamlead_dashboard(request):
    answers = EmployeeAnswer.objects.select_related('employee', 'question').all()
    return render(request, "survey/teamlead_dashboard.html", {"answers": answers})

@login_required
def employee_dashboard(request):
    forms = SurveyForm.objects.all()
    return render(request, "survey/employee_dashboard.html", {"forms": forms})


# ------------------------
# Create Survey Form
# ------------------------
@login_required
def create_form(request):
    if request.method == "POST":
        title = request.POST.get("title", "Survey Form")
        form = SurveyForm.objects.create(title=title, created_by=request.user)

        questions = request.POST.getlist("questions[]")
        types = request.POST.getlist("answer_type[]")
        options = request.POST.getlist("options[]")

        for i in range(len(questions)):
            Question.objects.create(
                form=form,
                text=questions[i],
                type=types[i],
                options=options[i] if types[i] == "choice" else ""
            )
        return redirect("survey:hr_dashboard")

    return render(request, "survey/create_form.html")


# ------------------------
# Fill Form (Employee)
# ------------------------
@login_required
def fill_form(request, id):
    form = get_object_or_404(SurveyForm, id=id)

    # Prepare choice options
    questions = []
    for q in form.questions.all():
        q.opts = [opt.strip() for opt in q.options.split(',')] if q.type == "choice" else []
        questions.append(q)

    if request.method == "POST":
        for q in form.questions.all():
            ans = request.POST.get(f'answer_{q.id}')
            if ans:
                EmployeeAnswer.objects.create(
                    employee=request.user,
                    question=q,
                    answer=ans
                )
        return redirect('survey:employee_dashboard')

    return render(request, "survey/employee_form.html", {"form": form, "questions": questions})


# ------------------------
# Results Table & Charts
# ------------------------
@login_required
def results_table(request):
    answers = EmployeeAnswer.objects.select_related("employee", "question").all()
    is_teamlead = request.user.groups.filter(name="TeamLead").exists()
    return render(request, "survey/results_table.html", {
        "results": answers,
        "is_teamlead": is_teamlead
    })


@login_required
def results_charts(request):
    charts = []
    for q in Question.objects.all():
        if q.type != "choice":
            continue
        answers = EmployeeAnswer.objects.filter(question=q)
        labels = [o.strip() for o in q.options.split(",") if o.strip()]
        values = [answers.filter(answer=opt).count() for opt in labels]
        charts.append({"question": q.text, "labels": labels, "values": values})

    charts_json = json.dumps(charts)
    return render(request, "survey/charts.html", {"charts": charts, "charts_json": charts_json})






# ------------------------
# Feedback (TeamLead only)
# ------------------------
def is_teamlead(user):
    return user.groups.filter(name='TeamLead').exists()

@login_required
@user_passes_test(is_teamlead)
def send_feedback(request):
    if request.method == "POST":
        answer_id = request.POST.get("answer_id")
        feedback_text = request.POST.get("feedback", "")
        
        if not answer_id:
            messages.error(request, "Answer ID missing!")
            return redirect("survey:results_table")
        
        ans = get_object_or_404(EmployeeAnswer, id=answer_id)
        ans.feedback = feedback_text
        ans.save()
        messages.success(request, "Feedback sent successfully.")
    
    return redirect("survey:results_table")


#___________________________
@login_required
def home(request):
    user = request.user
    context = {
        'show_hr': user.groups.filter(name='HR').exists(),
        'show_teamlead': user.groups.filter(name='TeamLead').exists(),
        'show_employee': user.groups.filter(name='Employee').exists(),
    }
    return render(request, "survey/home.html", context)
