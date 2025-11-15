from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import SurveyForm, Question, EmployeeAnswer
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
# ------------------------
# Home Redirect
# ------------------------
from django.shortcuts import redirect

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

@login_required
def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='HR').exists():
        return redirect('hr_dashboard')
    elif user.groups.filter(name='TeamLead').exists():
        return redirect('teamlead_dashboard')
    elif user.groups.filter(name='Employee').exists():
        return redirect('employee_dashboard')
    else:
        return redirect('login')  # fallback





# ------------------------
# User Registration
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign group
            group = Group.objects.get(name=form.cleaned_data['role'])
            user.groups.add(group)
            # Authenticate & login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)  # <-- This logs in the user
            # Redirect
            return redirect('redirect_after_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ------------------------
# Redirect after login
# ------------------------

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



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
        return redirect("hr_dashboard")

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
        return redirect('employee_dashboard')

    return render(request, "survey/employee_form.html", {"form": form, "questions": questions})

# ------------------------
# Results Table
# ------------------------
@login_required
def results_table(request):
    answers = EmployeeAnswer.objects.select_related("employee", "question").all()
    is_teamlead = request.user.groups.filter(name="TeamLead").exists()
    return render(request, "survey/results_table.html", {
        "results": answers,
        "is_teamlead": is_teamlead
    })

# ------------------------
# Results Charts
# ------------------------
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
        ans = get_object_or_404(EmployeeAnswer, id=answer_id)
        ans.feedback = feedback_text
        ans.save()
    return redirect("results_table")




