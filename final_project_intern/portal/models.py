from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    YEAR_CHOICES = [(1,"First Year"),(2,"Second Year"),(3,"Third Year"),(4,"Fourth Year")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    register_number = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, default="Computer Science with Cyber Security")
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=3)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.register_number}"

class AcademicRecord(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="academic")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    backlogs = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student} Academic Record"

class Company(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="companies/", blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    WORK_CHOICES = [("On-site","On-site"),("Hybrid","Hybrid"),("Remote","Remote")]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=150)
    description = models.TextField()
    package = models.CharField(max_length=60)
    skills_required = models.CharField(max_length=300)
    minimum_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    work_mode = models.CharField(max_length=20, choices=WORK_CHOICES, default="On-site")
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

class Application(models.Model):
    STATUS_CHOICES = [
        ("Applied","Applied"),("Under Review","Under Review"),
        ("Shortlisted","Shortlisted"),("Rejected","Rejected"),("Selected","Selected")
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student","job"], name="unique_student_job")
        ]

    def __str__(self):
        return f"{self.student} -> {self.job}"
