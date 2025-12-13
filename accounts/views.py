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
    from jobs.models import Application, SavedJob
    from skillmap.models import CandidateSkillProfile
    
    applied = Application.objects.filter(applicant=request.user).select_related('job')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    skill_profile = CandidateSkillProfile.objects.filter(
        github_username=request.user.profile.github_username,
        linkedin_username=request.user.profile.linkedin_username
    ).first()
    
    return render(request, 'accounts/candidate_dashboard.html', {
        'applied': applied, 
        'saved_jobs': saved_jobs,
        'skill_profile': skill_profile
    })

@login_required
def employer_dashboard(request):
    from jobs.models import Job, Application
    
    jobs = Job.objects.filter(company__icontains=request.user.profile.company_name or '')
    applications = Application.objects.filter(job__in=jobs).select_related('job', 'applicant')
    
    return render(request, 'accounts/employer_dashboard.html', {
        'jobs': jobs,
        'applications': applications
    })

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")