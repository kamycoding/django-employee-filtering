from datetime import date

from django.db.models import Avg
from django.shortcuts import render

from .models import Employee


def employee_overview(request):
    # 1. All employees; select_related loads each department in the same query
    all_employees = Employee.objects.select_related("department").all()

    # 2. Employees earning more than 3000 € per month (strictly greater)
    high_earners = Employee.objects.filter(salary__gt=3000)

    # 3. Number of employees earning 5000 € per month or more
    top_earner_count = Employee.objects.filter(salary__gte=5000).count()

    # 4. Average salary of the Sales department (None if Sales has no employees)
    sales_avg_salary = Employee.objects.filter(department__name="Sales").aggregate(
        avg_salary=Avg("salary")
    )["avg_salary"]

    # 5. Hired before 1 January 2022 and not in the HR department
    early_non_hr_employees = (
        Employee.objects.select_related("department")
        .filter(hire_date__lt=date(2022, 1, 1))
        .exclude(department__name="HR")
    )

    context = {
        "all_employees": all_employees,
        "high_earners": high_earners,
        "top_earner_count": top_earner_count,
        "sales_avg_salary": sales_avg_salary,
        "early_non_hr_employees": early_non_hr_employees,
    }
    return render(request, "employee_list.html", context)
