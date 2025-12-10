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
