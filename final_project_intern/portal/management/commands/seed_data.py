import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from portal.models import Application, Company, Job, StudentProfile

# ---------------------------------------------------------------------------
# Company data: (name, city, one-line description)
# Covers a wide mix of domains and places so Opportunities looks realistic.
# ---------------------------------------------------------------------------
COMPANIES = [
    ("Nova Cloud Systems", "Bengaluru", "Cloud infrastructure and DevOps tooling."),
    ("Finlytics Capital", "Mumbai", "Fintech analytics for retail banking."),
    ("MedixCare Health Tech", "Chennai", "Digital health records and telemedicine."),
    ("BrightPath EdTech", "Coimbatore", "Online learning platforms for schools."),
    ("Orbit Retail Labs", "Hyderabad", "E-commerce and supply-chain software."),
    ("SecureNet Cyber", "Pune", "Enterprise cybersecurity and threat intel."),
    ("Quantum Data Works", "Bengaluru", "Data engineering and applied AI."),
    ("Vertex Manufacturing", "Coimbatore", "Industrial automation and IoT."),
    ("PixelForge Studios", "Delhi NCR", "Product design and UI/UX consultancy."),
    ("Ceres AgriTech", "Coimbatore", "Precision agriculture and farm analytics."),
    ("Skyline Telecom", "Gurugram", "5G network software and telecom systems."),
    ("Meridian Consulting Group", "Mumbai", "Strategy and IT consulting."),
    ("GreenGrid Energy", "Chennai", "Renewable energy management platforms."),
    ("Zenith Logistics Tech", "Hyderabad", "Fleet and warehouse management software."),
    ("Harbor HR Solutions", "Kolkata", "HRMS and payroll automation."),
    ("Lumen Marketing Co", "Bengaluru", "Digital marketing and adtech."),
    ("Falcon Aerospace Systems", "Bengaluru", "Avionics and embedded software."),
    ("Northwind Insurance Tech", "Pune", "Insurance claims automation."),
]

# ---------------------------------------------------------------------------
# Job title pools per rough domain, so titles match each company's focus.
# ---------------------------------------------------------------------------
TITLES_BY_DOMAIN = {
    "software": ["Software Engineer", "Backend Developer", "Full Stack Developer", "Cloud Engineer", "DevOps Engineer", "QA Automation Engineer"],
    "data": ["Data Analyst", "Data Engineer", "Machine Learning Engineer", "Business Intelligence Analyst"],
    "security": ["Cybersecurity Analyst", "Security Engineer", "SOC Analyst"],
    "design": ["UI/UX Designer", "Product Designer", "Graphic Designer"],
    "product": ["Product Management Trainee", "Associate Product Manager", "Business Analyst"],
    "core": ["Embedded Systems Engineer", "Automation Engineer", "Network Engineer", "IoT Developer"],
    "finance": ["Financial Analyst", "Risk Analyst", "Investment Research Associate"],
    "marketing": ["Digital Marketing Associate", "SEO Specialist", "Marketing Analyst"],
    "hr": ["HR Associate", "Talent Acquisition Executive"],
    "consulting": ["Associate Consultant", "IT Consultant"],
    "support": ["Technical Support Engineer", "Customer Success Associate"],
}

DOMAIN_BY_COMPANY = {
    "Nova Cloud Systems": "software", "Finlytics Capital": "finance", "MedixCare Health Tech": "software",
    "BrightPath EdTech": "software", "Orbit Retail Labs": "product", "SecureNet Cyber": "security",
    "Quantum Data Works": "data", "Vertex Manufacturing": "core", "PixelForge Studios": "design",
    "Ceres AgriTech": "data", "Skyline Telecom": "core", "Meridian Consulting Group": "consulting",
    "GreenGrid Energy": "core", "Zenith Logistics Tech": "software", "Harbor HR Solutions": "hr",
    "Lumen Marketing Co": "marketing", "Falcon Aerospace Systems": "core", "Northwind Insurance Tech": "finance",
}

SKILLS_BY_DOMAIN = {
    "software": "Python, Django, REST APIs, Git, SQL",
    "data": "Python, SQL, Pandas, Machine Learning, Power BI",
    "security": "Networking, Linux, SIEM, Python, Ethical Hacking",
    "design": "Figma, Adobe XD, Wireframing, User Research",
    "product": "Communication, SQL, Analytics, Agile",
    "core": "C, Embedded C, IoT Protocols, MATLAB",
    "finance": "Excel, Financial Modeling, SQL, Accounting",
    "marketing": "SEO, Google Analytics, Content Strategy, Ads",
    "hr": "Communication, MS Office, Recruitment Tools",
    "consulting": "Problem Solving, Excel, Communication, PowerPoint",
    "support": "Communication, Troubleshooting, CRM Tools",
}

WORK_MODES = ["On-site"] * 4 + ["Hybrid"] * 3 + ["Remote"] * 3  # ~40/30/30 mix
PACKAGES = ["₹3.5 LPA", "₹4.2 LPA", "₹5 LPA", "₹6 LPA", "₹6.5 LPA", "₹7.5 LPA", "₹9 LPA", "₹12 LPA", "₹18 LPA"]

APPLICATION_STATUS_POOL = ["Applied", "Applied", "Under Review", "Shortlisted", "Rejected"]


class Command(BaseCommand):
    help = "Seeds demo companies, 50 job opportunities across domains/locations/work-modes, and sample applications (with 2 placements) for every registered student."

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-applications",
            action="store_true",
            help="Do not reset existing applications for students (jobs/companies are still reset).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.localdate()

        # --- reset opportunities so re-running gives a clean, consistent demo set ---
        Job.objects.all().delete()
        Company.objects.all().delete()

        companies = [
            Company.objects.create(name=name, location=city, description=desc)
            for name, city, desc in COMPANIES
        ]
        self.stdout.write(self.style.SUCCESS(f"Created {len(companies)} companies."))

        jobs = []
        target_total = 50
        # Give every company at least 2 jobs, then top up randomly to reach 50.
        base_count = {c.name: 2 for c in companies}
        remaining = target_total - sum(base_count.values())
        while remaining > 0:
            c = random.choice(companies)
            base_count[c.name] += 1
            remaining -= 1

        for company in companies:
            domain = DOMAIN_BY_COMPANY.get(company.name, "software")
            titles = TITLES_BY_DOMAIN[domain]
            skills = SKILLS_BY_DOMAIN[domain]
            for i in range(base_count[company.name]):
                title = titles[i % len(titles)]
                deadline = today + timedelta(days=random.randint(10, 120))
                job = Job.objects.create(
                    company=company,
                    title=title,
                    description=(
                        f"{company.name} is hiring a {title} to join our {company.location} team. "
                        f"You'll work on real-world problems in {company.description.lower()} "
                        f"and collaborate closely with cross-functional teams."
                    ),
                    package=random.choice(PACKAGES),
                    skills_required=skills,
                    minimum_cgpa=round(random.uniform(6.0, 8.5), 2),
                    work_mode=random.choice(WORK_MODES),
                    deadline=deadline,
                )
                jobs.append(job)

        self.stdout.write(self.style.SUCCESS(f"Created {len(jobs)} job opportunities."))
        remote = sum(1 for j in jobs if j.work_mode == "Remote")
        hybrid = sum(1 for j in jobs if j.work_mode == "Hybrid")
        onsite = sum(1 for j in jobs if j.work_mode == "On-site")
        self.stdout.write(f"  Work mode mix -> On-site: {onsite}, Hybrid: {hybrid}, Remote: {remote}")

        # --- seed applications for every registered student ---
        students = list(StudentProfile.objects.all())
        if not students:
            self.stdout.write(self.style.WARNING(
                "No student accounts exist yet. Register a student account, then re-run "
                "'python manage.py seed_data' to also seed applications and placements."
            ))
            return

        if not options["keep_applications"]:
            Application.objects.filter(student__in=students).delete()

        for student in students:
            sample_size = min(len(jobs), random.randint(7, 10))
            applied_jobs = random.sample(jobs, sample_size)

            for index, job in enumerate(applied_jobs):
                if index < 2:
                    status = "Selected"  # guarantee 2 default placements per student
                else:
                    status = random.choice(APPLICATION_STATUS_POOL)
                Application.objects.get_or_create(
                    student=student, job=job, defaults={"status": status}
                )

            self.stdout.write(self.style.SUCCESS(
                f"  {student.register_number}: applied to {sample_size} jobs, 2 marked as Selected (placed)."
            ))

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
