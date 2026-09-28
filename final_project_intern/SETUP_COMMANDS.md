# CORRECT SETUP COMMANDS — Windows PowerShell

# 1. MySQL Workbench — run once
DROP DATABASE IF EXISTS final_project_intern_db;
CREATE DATABASE final_project_intern_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 2. VS Code terminal — open the folder containing manage.py
python --version
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Create .env in the same folder as manage.py
# Put your actual MySQL password in DB_PASSWORD:
SECRET_KEY=change-this-secret-key
DEBUG=True
DB_NAME=final_project_intern_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=3306

# 4. Create/update Django database tables
python manage.py check
python manage.py makemigrations
python manage.py migrate

# 5. Create admin account
python manage.py createsuperuser

# 6. Start the project
python manage.py runserver

# 7. Open, then register a student account (Opportunities/Applications are
# empty until a student account exists)
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/

# 8. In a second terminal (keep runserver running), seed demo data: 50
# opportunities across many domains/locations/work-modes (Remote/Hybrid/
# On-site), plus sample applications with 2 auto-placed ("Selected") roles
# per student. Refresh the browser afterwards to see Opportunities,
# Applications and the Placed page populate.
# Safe to re-run any time — it refreshes the 50 opportunities and reseeds
# each student's applications (use --keep-applications to skip that part).
python manage.py seed_data

# 8. If port 8000 is busy
python manage.py runserver 8001

# 9. Verify data in MySQL Workbench
USE final_project_intern_db;
SHOW TABLES;
SELECT * FROM portal_studentprofile;
SELECT * FROM portal_academicrecord;
SELECT * FROM portal_company;
SELECT * FROM portal_job;
SELECT * FROM portal_application;
