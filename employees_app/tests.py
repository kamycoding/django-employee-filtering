from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Department, Employee


class EmployeeOverviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Same data as populate.py, created in the isolated test database
        sales = Department.objects.create(name="Sales")
        engineering = Department.objects.create(name="Engineering")
        hr = Department.objects.create(name="HR")
        marketing = Department.objects.create(name="Marketing")

        employees = [
            ("Max Müller", "3200.00", sales, date(2021, 3, 1)),
            ("Anna Schmidt", "2800.00", engineering, date(2022, 7, 10)),
            ("Clara Wagner", "4100.00", sales, date(2020, 6, 15)),
            ("David Fischer", "5000.00", engineering, date(2019, 1, 20)),
            ("Emma Becker", "2300.00", hr, date(2023, 1, 5)),
            ("Frank Zimmermann", "3900.00", marketing, date(2021, 11, 11)),
            ("Greta Meier", "3100.00", sales, date(2023, 8, 8)),
            ("Henry Schneider", "2700.00", hr, date(2022, 2, 2)),
        ]
        for name, salary, department, hire_date in employees:
            Employee.objects.create(
                name=name,
                salary=Decimal(salary),
                department=department,
                hire_date=hire_date,
            )

    def setUp(self):
        self.response = self.client.get(reverse("employee_overview"))

    def names(self, key):
        return {employee.name for employee in self.response.context[key]}

    def test_page_renders(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "employee_list.html")

    def test_all_employees(self):
        self.assertEqual(len(self.response.context["all_employees"]), 8)

    def test_employees_earning_more_than_3000(self):
        self.assertEqual(
            self.names("high_earners"),
            {"Max Müller", "Clara Wagner", "David Fischer", "Frank Zimmermann", "Greta Meier"},
        )

    def test_count_earning_5000_or_more_includes_exactly_5000(self):
        self.assertEqual(self.response.context["top_earner_count"], 1)

    def test_sales_average_salary_rounded(self):
        self.assertEqual(
            round(self.response.context["sales_avg_salary"], 2), Decimal("3466.67")
        )
        self.assertContains(self.response, "3466.67 €")

    def test_hired_before_2022_excluding_hr(self):
        self.assertEqual(
            self.names("early_non_hr_employees"),
            {"Max Müller", "Clara Wagner", "David Fischer", "Frank Zimmermann"},
        )
