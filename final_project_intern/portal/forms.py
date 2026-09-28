from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile, AcademicRecord


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80, required=False)
    email = forms.EmailField()
    register_number = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "register_number", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_register_number(self):
        value = self.cleaned_data["register_number"].strip().upper()
        if StudentProfile.objects.filter(register_number__iexact=value).exists():
            raise forms.ValidationError("Register number already exists.")
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].strip().lower()
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data.get("last_name", "").strip()
        user.email = self.cleaned_data["email"].strip().lower()
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ("register_number", "phone", "department", "year", "bio", "skills", "avatar", "resume")
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

    def clean_register_number(self):
        return self.cleaned_data["register_number"].strip().upper()


class AcademicForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ("cgpa", "tenth_percentage", "twelfth_percentage", "backlogs")

    def clean_cgpa(self):
        value = self.cleaned_data["cgpa"]
        if value < 0 or value > 10:
            raise forms.ValidationError("CGPA must be between 0 and 10.")
        return value

    def clean_tenth_percentage(self):
        value = self.cleaned_data["tenth_percentage"]
        if value < 0 or value > 100:
            raise forms.ValidationError("10th percentage must be between 0 and 100.")
        return value

    def clean_twelfth_percentage(self):
        value = self.cleaned_data["twelfth_percentage"]
        if value < 0 or value > 100:
            raise forms.ValidationError("12th percentage must be between 0 and 100.")
        return value
