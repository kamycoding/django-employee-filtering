# Django Employee Filtering

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django&logoColor=white)](https://docs.djangoproject.com/en/5.2/)
[![SQLite](https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/tests-6%20passing-brightgreen)](#testing)

A small Django application that uses the Django ORM to query, filter and aggregate employee data and render the results in a server-side template.

This is an exercise from the backend training program at Developer Akademie. Its goal is to practise writing clear, correct QuerySets, not to build a full-featured application.

## Features

A single page answers five questions about the sample dataset:

1. **All employees**: lists every employee with their department and salary.
2. **High earners**: lists employees who earn more than €3,000 per month.
3. **Top earner count**: counts employees who earn €5,000 or more per month.
4. **Sales average**: calculates the average salary in the Sales department and shows it rounded to two decimal places.
5. **Early hires outside HR**: lists employees hired before 1 January 2022 who are not in the HR department.

> The page itself is in German, because the original assignment was written in German.

## Django ORM Concepts

All queries are in [`employees_app/views.py`](employees_app/views.py).

| Concept                 | Usage in this project                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| Field lookups           | `salary__gt=3000`, `salary__gte=5000`, `hire_date__lt=date(2022, 1, 1)`                                   |
| Filtering and exclusion | `.filter(...)` narrows a QuerySet and `.exclude(department__name="HR")` removes matches                   |
| Counting                | `.count()` runs a `SELECT COUNT(*)` in the database instead of loading rows                               |
| Aggregation             | `.aggregate(avg_salary=Avg("salary"))` calculates the Sales average in a single query                     |
| Relationships           | `Employee.department` is a `ForeignKey` to `Department`; `department__name` follows it in lookups         |
| `select_related`        | Loads each employee's department through a SQL join, so the template does not run one extra query per row |

The edge cases are handled explicitly:

- "More than €3,000" uses `gt`, so an employee who earns exactly €3,000 is not included.
- "€5,000 or more" uses `gte`, so an employee who earns exactly €5,000 is counted.
- If Sales has no employees, the average is `None`, and the template shows a fallback message instead of an empty value.

## Data Model

```text
Department                Employee
----------                --------
id                        id
name                      name
                          salary       (Decimal, 2 places)
                          hire_date    (Date)
                          department → Department (ForeignKey)
```

## Getting Started

These instructions apply to **Ubuntu/Linux** and **macOS**.

### Prerequisites

- Python 3.10 or newer
- `git`

On Ubuntu, you may need to install the `venv` module first:

```bash
sudo apt install python3-venv
```

On macOS, install Python 3 from [python.org](https://www.python.org/downloads/) or with Homebrew (`brew install python`).

### Installation

Clone the repository and change into the project directory:

```bash
git clone https://github.com/kamycoding/django-employee-filtering.git
cd django-employee-filtering
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Database Setup

Apply the migrations to create the SQLite database (`db.sqlite3`):

```bash
python manage.py migrate
```

Seed the database with the sample departments and employees:

```bash
python manage.py shell < populate.py
```

> Run the seed script only once. Running it again inserts duplicate records. To start over, delete `db.sqlite3`, then run `migrate` and the seed script again.

### Run the Development Server

```bash
python manage.py runserver
```

Then open the application in your browser:

**<http://127.0.0.1:8000/employees/>**

## Testing

Run the test suite:

```bash
python manage.py test employees_app
```

The tests in [`employees_app/tests.py`](employees_app/tests.py) use Django's `TestCase`. They create the same data as `populate.py` in an isolated test database, so you don't need to seed the database first.

| Test                                                    | What it checks                                                    |
| ------------------------------------------------------- | ----------------------------------------------------------------- |
| `test_page_renders`                                     | The page returns HTTP 200 and uses `employee_list.html`           |
| `test_all_employees`                                    | All 8 employees are included                                      |
| `test_employees_earning_more_than_3000`                 | Only employees who earn strictly more than €3,000 are returned    |
| `test_count_earning_5000_or_more_includes_exactly_5000` | An employee who earns exactly €5,000 is counted                   |
| `test_sales_average_salary_rounded`                     | The Sales average is 3466.67 and the page shows it as `3466.67 €` |
| `test_hired_before_2022_excluding_hr`                   | Hire date and department are filtered correctly                   |

## Project Structure

```text
.
├── core/                        # Project configuration (settings, root URLs, WSGI/ASGI)
├── employees_app/
│   ├── migrations/              # Database schema for Department and Employee
│   ├── templates/
│   │   └── employee_list.html   # Assignment page and results
│   ├── models.py                # Department and Employee models
│   ├── tests.py                 # Automated tests
│   ├── urls.py                  # Routes /employees/ to the view
│   └── views.py                 # ORM queries
├── manage.py
├── populate.py                  # Sample data seed script
└── requirements.txt
```

## Credits

This project is based on the starter repository provided by Developer Akademie:
[Developer-Akademie-AA/BE_staff_filter_app_teilnehmer](https://github.com/Developer-Akademie-AA/BE_staff_filter_app_teilnehmer)

**Provided by the starter repository**

- Django project setup (`core/`, `manage.py`, `requirements.txt`)
- `Department` and `Employee` models and the initial migration
- URL routing for `/employees/`
- Sample data script (`populate.py`)
- Template with the assignment questions
- An empty `employee_overview` view

**Added in this repository**

- The ORM queries for all five questions in `employees_app/views.py`
- The results section of `employee_list.html`, including fallback messages for empty results
- The six automated tests in `employees_app/tests.py`
- This README

## Author

**kamycoding**: [github.com/kamycoding](https://github.com/kamycoding)
