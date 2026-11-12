# Django Employee Filtering

A Django backend exercise developed as part of the Developer Akademie training program.

The project demonstrates how to use Django ORM QuerySets to retrieve, filter, and aggregate employee data and display the results using Django templates.

## Technologies

- Python
- Django 5.2.7
- SQLite
- Django ORM
- Django Templates

## Features

The application implements five exercises:

1. Display all employees with their department and salary.
2. List employees earning more than €3,000 per month.
3. Count employees earning €5,000 or more per month.
4. Calculate the average salary in the Sales department, rounded to two decimal places.
5. List employees hired before January 1, 2022, excluding the HR department.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/kamycoding/django-employee-filtering.git
cd django-employee-filtering
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Populate the database with sample data (run once):

```bash
python manage.py shell < populate.py
```

Start the development server:

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/employees/

## Running Tests

```bash
python manage.py test employees_app
```

The project includes six automated tests covering the page response and the five filtering exercises.

## Project Structure

```text
core/                    # Django project configuration
employees_app/
  models.py              # Employee and Department models
  views.py               # ORM queries and view logic
  tests.py               # Automated tests
  templates/
    employee_list.html   # Employee results
populate.py              # Sample data
manage.py
requirements.txt
```

## Notes

This is an educational backend project. The focus is on Django ORM queries and clean, readable code rather than frontend styling.
