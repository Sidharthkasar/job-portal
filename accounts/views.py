from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from .forms import SignUpForm, LoginForm, CandidateProfileForm, EmployerProfileForm
from .models import Profile
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login after register
            login(request, user)
            messages.success(request, "Registration successful.")
            # redirect based on role
            role = user.profile.role
            if role == 'employer':
                return redirect('employer_dashboard')
            return redirect('candidate_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect based on role
            role = user.profile.role
            if role == 'employer':
                return redirect('employer_dashboard')
            return redirect('candidate_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('job_list')

@login_required
def profile_view(request):
    profile = request.user.profile
    if profile.role == 'candidate':
        form = CandidateProfileForm(request.POST or None, request.FILES or None, instance=profile)
    else:
        form = EmployerProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

@login_required
def candidate_dashboard(request):
    # You likely have an Application model — fetch applied jobs by this user
    # Example: from jobs.models import JobApplication
    # applied = JobApplication.objects.filter(candidate=request.user)
    applied = []  # placeholder; replace with real queryset
    saved_jobs = []  # placeholder if you implement saved jobs
    return render(request, 'accounts/candidate_dashboard.html', {'applied': applied, 'saved_jobs': saved_jobs})

@login_required
def employer_dashboard(request):
    # employer should see jobs they've posted and counts of applications per job
    # Example: jobs = Job.objects.filter(posted_by=request.user)  # if you tracked that
    jobs = []  # placeholder; replace with real queryset
    return render(request, 'accounts/employer_dashboard.html', {'jobs': jobs})

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")