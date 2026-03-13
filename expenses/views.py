from django.contrib.auth.decorators import login_required
from users.models import Profile
from utils.csv_exporter import export_expenses_csv
from django.db.models.functions import TruncMonth
import json
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Department, Expense
from django.db.models import Sum
# aiLogic
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
# emilNotification
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


@login_required
def dashboard(request):

    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_count = Expense.objects.count()

    # STATUS COUNTS
    pending = Expense.objects.filter(status="pending").count()
    approved = Expense.objects.filter(status="approved").count()
    rejected = Expense.objects.filter(status="rejected").count()

    # CATEGORY CHART
    category_data = Expense.objects.values('category__name').annotate(
        total=Sum('amount')
    )

    categories = [item['category__name'] for item in category_data]
    totals = [float(item['total']) for item in category_data]

    # MONTHLY CHART
    monthly_data = Expense.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total=Sum('amount')).order_by('month')

    months = [str(item['month'])[:7] for item in monthly_data]
    monthly_totals = [float(item['total']) for item in monthly_data]
    # DEPARTMENT EXPENSE CHART
        # ---------------------------

    department_data = Expense.objects.values('department__name').annotate(
            total=Sum('amount')
        )

    dept_labels = [d['department__name'] for d in department_data]
    dept_totals = [float(d['total']) for d in department_data]

    recent_expenses = Expense.objects.order_by('-created_at')[:5]
    # Ai logic

    today = now()
    last_month = today - timedelta(days=30)

    current_total = Expense.objects.filter(
        date__gte=last_month
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    previous_total = Expense.objects.filter(
        date__lt=last_month
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    insight = ""

    if current_total > previous_total:
        insight = "⚠ Spending increased compared to last month."
    elif current_total < previous_total:
        insight = "✅ Spending decreased compared to last month."
    else:
     insight = "Spending unchanged."

    context = {
        'total_expense': total_expense,
        'expense_count': expense_count,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,

        'categories': json.dumps(categories),
        'totals': json.dumps(totals),

        'months': json.dumps(months),
        'monthly_totals': json.dumps(monthly_totals),

        'dept_labels': json.dumps(dept_labels),
        'dept_totals': json.dumps(dept_totals),

        'recent_expenses': recent_expenses,
        "context_insight": insight
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_expense(request):

    categories = Category.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":

        title = request.POST['title']
        amount = request.POST['amount']
        # category_id = request.POST['category']
        # department_id = request.POST['department']
        category_id = request.POST.get('category')
        department_id = request.POST.get('department')
        date = request.POST['date']
        description = request.POST['description']
        receipt = request.FILES.get("receipt")

        Expense.objects.create(
            title=title,
            amount=amount,
            category_id=category_id,
            department_id=department_id,
            employee=request.user,
            date=date,
            description=description,
            receipt=receipt
        )

        return redirect('/expenses/')

    return render(request,'add_expense.html',{
        'categories':categories,
        'departments':departments
    })

@login_required
def expense_list(request):

    category = request.GET.get('category')
    if request.user.profile.role == "employee":
        expenses = Expense.objects.filter(employee=request.user)
    else:
        expenses = Expense.objects.all()
    expenses = Expense.objects.all().order_by('-date')

    if category:
        expenses = expenses.filter(category_id=category)

    categories = Category.objects.all()

    return render(request,'expense_list.html',{
        'expenses':expenses,
        'categories':categories
    })

# exporter
@login_required
def export_csv(request):

    return export_expenses_csv()
    
@login_required
def approve_expense(request, id):
     # ROLE CHECK
    if request.user.profile.role != "manager":
        return redirect("/")
    
    expense = Expense.objects.get(id=id)

    expense.status = "approved"

    expense.save()
    send_mail(
        "Expense Approved",
        f"Your expense '{expense.title}' was approved.",
        settings.EMAIL_HOST_USER,
        [expense.employee.email],
        fail_silently=True
    )
    return redirect('/expenses/')

@login_required
def reject_expense(request, id):
     # ROLE CHECK
    if request.user.profile.role != "manager":
        return redirect("/")
    expense = Expense.objects.get(id=id)

    expense.status = "rejected"

    expense.save()
    send_mail(
    "Expense Rejected",
    f"Your expense '{expense.title}' was rejected.",
    settings.EMAIL_HOST_USER,
    [expense.employee.email],
    fail_silently=True
)

    return redirect('/expenses/')
# category
def category_list(request):

    categories = Category.objects.all()

    return render(request,"categories.html",{
        "categories":categories
    })

# Approve
@login_required
def approvals(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.user.profile.role != "manager":
        return redirect("/")

    expenses = Expense.objects.filter(status="pending")

    return render(request,"approvals.html",{
        "expenses":expenses
    })

# AddCategory
def add_category(request):

    if request.method == "POST":

        name = request.POST["name"]
        description = request.POST["description"]

        Category.objects.create(
            name=name,
            description=description
        )

        return redirect("/categories/")

    return render(request,"add_category.html")

# emailNotification

# Department
def department_list(request):

    departments = Department.objects.all()

    return render(request, "department.html", {
        "departments": departments
    })


def add_department(request):

    if request.method == "POST":
        name = request.POST.get("name")
        Department.objects.create(name=name)
        return redirect("/departments")

    return render(request, "add_department.html")


def edit_department(request, id):

    department = Department.objects.get(id=id)

    if request.method == "POST":
        department.name = request.POST.get("name")
        department.save()

        return redirect("/departments")

    return render(request, "edit_department.html", {
        "department": department
    })


def delete_department(request, id):

    department = get_object_or_404(Department, id=id)
    department.delete()
    messages.success(request, "Department deleted successfully")

    return redirect("/departments")

