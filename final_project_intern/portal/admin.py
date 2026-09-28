from django.contrib import admin
from .models import AcademicRecord, Application, Company, Job, StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("register_number","user","department","year","phone")
    search_fields = ("register_number","user__username","user__email")

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ("student","cgpa","backlogs")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name","location")
    search_fields = ("name","location")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title","company","package","minimum_cgpa","deadline","work_mode")
    list_filter = ("work_mode","company")
    search_fields = ("title","company__name")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student","job","status","applied_at")
    list_filter = ("status",)
    search_fields = ("student__register_number","job__title")
