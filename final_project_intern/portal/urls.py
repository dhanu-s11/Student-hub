from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    PortalLoginView, academics_view, applications_view, dashboard,
    job_detail, jobs_view, placed_view, profile_view, register_view
)

urlpatterns = [
    path("", dashboard, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", PortalLoginView.as_view(), name="login"),
    path("register/", register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("academics/", academics_view, name="academics"),
    path("jobs/", jobs_view, name="jobs"),
    path("jobs/<int:pk>/", job_detail, name="job_detail"),
    path("applications/", applications_view, name="applications"),
    path("placed/", placed_view, name="placed"),
]
