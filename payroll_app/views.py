from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
import datetime
import calendar
from django.contrib import messages  

from .form import CustomUserLoginForm, CustomUserSignupForm
from .models import CustomUser, Attendance, Salary


def signup_view(request):
    form = CustomUserSignupForm()
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('dashboard')
    return render(request, 'signup.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(user.role)
            
            if user.role == "employee" or user.role == "Employee":
                today = timezone.now()
                
                att = Attendance.objects.filter(employee_name=user, time__date=today.date())
                print(att)
                if not att.exists():
                    
                    weekday = today.date().isoweekday()
                    if weekday in (6, 7):  # Saturday or Sunday
                        Attendance.objects.create(employee_name=user, time=today, status="holiday")
                    else:
                        Attendance.objects.create(employee_name=user, time=today, status="present")
            return redirect('dashboard')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    today = datetime.datetime.now()
    
    days_in_month = calendar.monthrange(today.year, today.month)[1]

    
    total_working_days = sum(1 for day in range(1, days_in_month + 1)
                             if datetime.date(today.year, today.month, day).weekday() < 5)

    today_date = datetime.date(today.year, today.month, today.day)

    if user.role.lower() == "employee":
        tillnow_working_days = sum(1 for day in range(1, today_date.day)
                                   if datetime.date(today.year, today.month, day).weekday() < 5)+1

        present = Attendance.objects.filter(employee_name=user, time__month=today.month, time__year=today.year,status="present")
        present_days = present.count()
        absent_days = tillnow_working_days - present_days
        upcoming_working_days = total_working_days - tillnow_working_days

        context = {
            "emp_id": user.id,
            "total_year": today.year,
            "today_month": today.month,
            "total_days": total_working_days,
            "tillnow_working_days": tillnow_working_days,
            "upcoming_working_days": upcoming_working_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "user_name": user.username,
            "Role": user.role,
        }

        if request.method == "POST":
            print("sal")
            if request.POST.get("action") == "show":
                salaries = Salary.objects.filter(employee_name=user).order_by('-year', '-month')
                context["salaries"] = salaries
            elif request.POST.get("action") =="hide":
                context["salaries"] = None

        return render(request, 'dashboard.html', context)

    elif user.role.lower() == "admin":
        employees = CustomUser.objects.filter(role__iexact='employee')
        emp_data = []

        for emp in employees:
            present = Attendance.objects.filter(employee_name=emp, time__month=today.month, time__year=today.year)
            present_days = present.count()
            absent_days = total_working_days - present_days

            sal_details = Salary.objects.filter(employee_name=emp, month=today_date.month, year=today_date.year).first()

            emp_data.append({
                "emp_name": emp.username,
                "emp_id": emp.id,
                "present_days": present_days,
                "absent_days": absent_days,
                "salary_status": bool(sal_details),
                "salary_amount": sal_details.salary_amount if sal_details else None,
            })

        return render(request, "dashboard.html", {"Role": "admin", "employees": emp_data})

    return HttpResponse("Nothing to display")


@login_required
def generate_salary(request):
    today_date = datetime.datetime.today()

    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        emp_name = request.POST.get("emp_name")
        pnt_days = int(request.POST.get("present_days", 0))
        abnt_days = int(request.POST.get("absent_days", 0))

        emp = get_object_or_404(CustomUser, id=emp_id)

        salary_amount = pnt_days * (emp.basic_salary / 30)

        salary_exists = Salary.objects.filter(
            employee_name=emp,
            month=today_date.month,
            year=today_date.year
        ).exists()

        if not salary_exists:
            today = timezone.now()
            print(today.month)
            if (today.month == 2 and today.day>=28) or today.day >= 30:
                Salary.objects.create(
                    employee_name=emp,
                    present_days=pnt_days,
                    absent_days=abnt_days,
                    month=today_date.month,
                    year=today_date.year,
                    salary_amount=salary_amount,
                )
                messages.success(request, f"Salary generated for {emp_name}")
            else:
                messages.warning(request, "Month is not completed yet.")
        else:
            messages.error(request, f"Salary already generated for {emp_name} this month.")

        return redirect("dashboard")



@login_required
def download_payslip(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id, employee_name=request.user)
    template = get_template('payslip.html')
    html = template.render({'salary': salary})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{salary.month}_{salary.year}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


@login_required
def delete_employee(request, emp_id):
    user = request.user
    if user.role.lower() != "admin":
        return HttpResponse("Unauthorized", status=401)
    
    emp = get_object_or_404(CustomUser, id=emp_id, role__iexact='employee')

    if request.method == "POST":
        emp.delete()
        messages.success(request, f"Employee {emp.username} deleted successfully.")
        return redirect('dashboard')
    
    return HttpResponse()







     
        
   



 
 
    