from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AcademicForm, ProfileForm, RegisterForm
from .models import AcademicRecord, Application, Job, StudentProfile


def get_student_profile(user):
    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={"register_number": f"TEMP-{user.pk}"},
    )
    academic, _ = AcademicRecord.objects.get_or_create(student=profile)
    return profile, academic


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
                profile = StudentProfile.objects.create(
                    user=user,
                    register_number=form.cleaned_data["register_number"],
                )
                AcademicRecord.objects.create(student=profile)
        except IntegrityError:
            form.add_error("register_number", "This register number is already registered.")
        else:
            login(request, user)
            messages.success(request, "Welcome to Student Hub!")
            return redirect("dashboard")

    return render(request, "portal/register.html", {"form": form})


class PortalLoginView(LoginView):
    template_name = "portal/login.html"
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    profile, academic = get_student_profile(request.user)

    jobs = (
        Job.objects.select_related("company")
        .filter(deadline__gte=timezone.localdate())
        .order_by("deadline", "title")[:4]
    )
    applications = (
        Application.objects.select_related("job", "job__company")
        .filter(student=profile)
        .order_by("-applied_at")[:5]
    )

    profile_fields = [
        profile.phone,
        profile.department,
        profile.year,
        profile.bio,
        profile.skills,
        profile.resume,
    ]
    academic_fields = [
        academic.cgpa,
        academic.tenth_percentage,
        academic.twelfth_percentage,
    ]
    filled = sum(bool(value) for value in profile_fields + academic_fields)
    completion = round(filled / (len(profile_fields) + len(academic_fields)) * 100)

    shortlisted_count = profile.applications.filter(status="Shortlisted").count()
    placed_count = profile.applications.filter(status="Selected").count()

    return render(request, "portal/dashboard.html", {
        "profile": profile,
        "academic": academic,
        "jobs": jobs,
        "applications": applications,
        "completion": completion,
        "shortlisted_count": shortlisted_count,
        "placed_count": placed_count,
    })


@login_required
def profile_view(request):
    profile, academic = get_student_profile(request.user)

    profile_form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
    )
    academic_form = AcademicForm(
        request.POST or None,
        instance=academic,
    )

    if request.method == "POST" and profile_form.is_valid() and academic_form.is_valid():
        profile_form.save()
        academic_form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "portal/profile.html", {
        "profile": profile,
        "profile_form": profile_form,
        "academic_form": academic_form,
    })


@login_required
def jobs_view(request):
    q = request.GET.get("q", "").strip()
    jobs = (
        Job.objects.select_related("company")
        .filter(deadline__gte=timezone.localdate())
        .order_by("deadline", "title")
    )
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q)
            | Q(company__name__icontains=q)
            | Q(skills_required__icontains=q)
            | Q(company__location__icontains=q)
        )

    return render(request, "portal/jobs.html", {"jobs": jobs, "q": q})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job.objects.select_related("company"), pk=pk)
    profile, _ = get_student_profile(request.user)
    applied = Application.objects.filter(student=profile, job=job).exists()
    expired = job.deadline < timezone.localdate()

    if request.method == "POST":
        if expired:
            messages.error(request, "The application deadline has passed.")
        elif applied:
            messages.info(request, "You have already applied for this role.")
        else:
            try:
                Application.objects.create(student=profile, job=job)
            except IntegrityError:
                messages.info(request, "You have already applied for this role.")
            else:
                messages.success(request, "Application submitted successfully.")
                return redirect("applications")

    return render(request, "portal/job_detail.html", {
        "job": job,
        "applied": applied,
        "expired": expired,
    })


@login_required
def applications_view(request):
    profile, _ = get_student_profile(request.user)
    applications = (
        Application.objects.select_related("job", "job__company")
        .filter(student=profile)
        .order_by("-applied_at")
    )
    return render(request, "portal/applications.html", {"applications": applications})


@login_required
def placed_view(request):
    profile, _ = get_student_profile(request.user)
    placements = (
        Application.objects.select_related("job", "job__company")
        .filter(student=profile, status="Selected")
        .order_by("-applied_at")
    )
    return render(request, "portal/placed.html", {"placements": placements})


@login_required
def academics_view(request):
    profile, academic = get_student_profile(request.user)
    return render(request, "portal/academics.html", {
        "profile": profile,
        "academic": academic,
    })
