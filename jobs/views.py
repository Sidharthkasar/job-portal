from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import JobForm
from .models import Job

# List all jobs
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# Job detail page
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Create a new job
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    
    return render(request, 'jobs/create_job.html', {'form': form})
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            messages.success(request, "Your application has been submitted!")
            return redirect("job_detail", job_id=job_id)
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html", {"job": job, "form": form})



from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Example context data - you can customize this as needed
    context = {
        'recent_applications': [],  # Fetch from the database
        'saved_jobs': [],  # Fetch from the database
        'notifications': [],  # Fetch from the database
    }
    return render(request, 'jobs/dashboard.html', context)