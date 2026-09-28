# Student Hub — Secure Student Management & Placement Portal

A Django + MySQL full-stack project for a college internship/viva. The UI follows an original implementation inspired by the visual direction of the supplied Dribbble student portal reference: light theme, vibrant blue accent, minimalist cards, spacious layout.

## 1. Requirements
- Python 3.11+ recommended
- MySQL Server 8.x
- MySQL Workbench (optional)
- VS Code recommended

## 2. Create database
In MySQL Workbench SQL Editor:
CREATE DATABASE final_project_intern_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

## 3. Open terminal in this folder
Windows PowerShell:
cd path\to\final_project_intern

## 4. Virtual environment
python -m venv venv
venv\Scripts\activate

## 5. Install packages
python -m pip install --upgrade pip
pip install -r requirements.txt

## 6. Environment file
Copy `.env.example` to `.env`.
Set DB_PASSWORD to your MySQL root password.

Example:
SECRET_KEY=change-this-secret-key
DEBUG=True
DB_NAME=final_project_intern_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=3306

## 7. Create tables
python manage.py makemigrations
python manage.py migrate

## 8. Create admin
python manage.py createsuperuser

## 9. Start server
python manage.py runserver

Open http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

## 10. Seed demo data (opportunities, applications, placements)
Opportunities/Applications/Placed pages are empty on a fresh database — there's
no data until you add some. Fastest way:
1. Register at least one student account in the browser.
2. In a terminal (with the venv active), run:
   python manage.py seed_data
   This creates 50 job opportunities across many companies, domains, and
   locations, each tagged On-site / Hybrid / Remote, plus a set of sample
   applications per student — including 2 guaranteed "Selected" (placed) roles.
3. Refresh the student portal: Opportunities, Applications, and the new
   Placed page (dashboard stat card, or the sidebar) will now show data.
4. Safe to re-run any time — it refreshes the 50 opportunities and reseeds
   each student's applications. Pass `--keep-applications` to only refresh
   opportunities and leave existing applications untouched.

## 11. First manual demo (optional, in addition to seeding)
1. Open My Profile and enter academic details.
2. Login to /admin/.
3. Add Company.
4. Add Job.
5. Return to student portal.
6. Open Opportunities.
7. Apply to a job.
8. Open Applications.
9. In admin, change application status to Shortlisted/Selected.
10. Refresh student Applications page (Selected roles also appear under Placed).

## Troubleshooting
- `No module named django`: activate venv and run `pip install -r requirements.txt`
- `No module named MySQLdb`: install MySQL client/build prerequisites or use a compatible Python/MySQL setup.
- `Access denied for user root`: check DB_USER and DB_PASSWORD in .env.
- `Unknown database`: create final_project_intern_db in MySQL Workbench.
- `Can't connect to MySQL server`: start the MySQL80 service in Windows Services.
- Port 8000 busy: python manage.py runserver 8001

## Important
Never commit `.env` or real passwords to GitHub.
