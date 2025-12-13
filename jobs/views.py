from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .forms import JobForm, ApplicationForm
from .models import Job, Application, SavedJob, InterviewSession, InterviewQuestion, InterviewResponse

# List all jobs with search filters
def job_list(request):
    jobs = Job.objects.all()
    
    # Search filters
    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    min_salary = request.GET.get('min_salary')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(company__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    if min_salary:
        try:
            jobs = jobs.filter(salary__gte=int(min_salary))
        except ValueError:
            pass
    
    context = {
        'jobs': jobs,
        'query': query,
        'location': location,
        'job_type': job_type,
        'min_salary': min_salary,
    }
    return render(request, 'jobs/job_list.html', context)

# Job detail page
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    
    context = {
        'job': job,
        'is_saved': is_saved,
    }
    return render(request, 'jobs/job_detail.html', context)

# Create a new job
@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_detail', job_id=job.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    
    return render(request, 'jobs/create_job.html', {'form': form})

# Apply to job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been submitted!")
            return redirect("job_detail", job_id=job_id)
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html", {"job": job, "form": form})

# Save/unsave job
@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved_job.delete()
        messages.success(request, "Job removed from saved jobs.")
    else:
        messages.success(request, "Job saved successfully!")
    
    return redirect('job_detail', job_id=job_id)

# Dashboard
@login_required
def dashboard(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'employer':
        # Employer dashboard - show all jobs if no company specified, or filter by company
        employer_company = request.user.profile.company_name or ""
        if employer_company.strip():
            jobs = Job.objects.filter(company__icontains=employer_company)
        else:
            # If no company specified, show all jobs (for testing) or jobs posted by this user
            jobs = Job.objects.all()[:10]  # Limit for testing

        applications = Application.objects.filter(job__in=jobs).order_by('-applied_at')
        context = {
            'jobs': jobs,
            'applications': applications,
        }
        return render(request, 'jobs/employer_dashboard.html', context)
    else:
        # Candidate dashboard
        applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
        saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
        context = {
            'applications': applications,
            'saved_jobs': saved_jobs,
        }
        return render(request, 'jobs/dashboard.html', context)


# Interview System Views
@login_required
def start_interview(request, application_id):
    """Start a new interview session for a job application"""
    from .models import InterviewSession
    from .utils import create_sample_questions

    application = get_object_or_404(Application, id=application_id, applicant=request.user)

    # Check if interview already exists
    existing_session = InterviewSession.objects.filter(
        candidate=request.user,
        job_application=application
    ).first()

    if existing_session:
        return redirect('interview_session', session_id=existing_session.id)

    # Create sample questions if they don't exist
    create_sample_questions()

    # Create new interview session
    session = InterviewSession.objects.create(
        candidate=request.user,
        job_application=application,
        total_questions=5  # Configurable
    )

    return redirect('interview_session', session_id=session.id)


@login_required
def interview_session(request, session_id):
    """Main interview interface"""
    from .models import InterviewSession, InterviewResponse
    from .utils import InterviewEngine

    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)

    if session.status == 'completed':
        # Show results
        engine = InterviewEngine(session)
        final_score = engine.calculate_final_score()
        skill_breakdown = engine.get_skill_breakdown()

        context = {
            'session': session,
            'final_score': final_score,
            'skill_breakdown': skill_breakdown,
            'responses': InterviewResponse.objects.filter(interview_session=session).select_related('question'),
        }
        return render(request, 'jobs/interview_results.html', context)

    # Get next question
    engine = InterviewEngine(session)
    question = engine.get_next_question()

    if not question:
        # No more questions - complete interview
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()
        return redirect('interview_session', session_id=session.id)

    # Check if question already answered
    existing_response = InterviewResponse.objects.filter(
        interview_session=session,
        question=question
    ).first()

    if existing_response:
        # Question already answered, get next one
        question = engine.get_next_question()
        if not question:
            session.status = 'completed'
            session.completed_at = timezone.now()
            session.save()
            return redirect('interview_session', session_id=session.id)

    context = {
        'session': session,
        'question': question,
        'question_number': session.questions_asked.count() + 1,
        'total_questions': session.total_questions,
        'progress': (session.questions_asked.count() / session.total_questions) * 100,
    }
    return render(request, 'jobs/interview_session.html', context)


@login_required
def submit_answer(request, session_id):
    """Submit answer to interview question"""
    from .models import InterviewSession, InterviewResponse
    from django.utils import timezone

    if request.method != 'POST':
        return redirect('interview_session', session_id=session_id)

    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)
    question_id = request.POST.get('question_id')
    answer = request.POST.get('answer', '').strip()

    if not question_id or not answer:
        messages.error(request, 'Please provide an answer.')
        return redirect('interview_session', session_id=session_id)

    question = get_object_or_404(InterviewQuestion, id=question_id)

    # Create response
    response, created = InterviewResponse.objects.get_or_create(
        interview_session=session,
        question=question,
        defaults={
            'candidate_answer': answer,
            'score': 3,  # Default score, can be improved with AI evaluation
        }
    )

    if not created:
        # Update existing answer
        response.candidate_answer = answer
        response.save()

    # Check if interview is complete
    if session.questions_asked.count() >= session.total_questions:
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()
        messages.success(request, 'Interview completed! Check your results.')
    else:
        messages.success(request, 'Answer submitted successfully.')

    return redirect('interview_session', session_id=session_id)


@login_required
def update_application_status(request, application_id):
    """Update application status in hiring funnel"""
    if request.method != 'POST':
        return redirect('dashboard')

    application = get_object_or_404(Application, id=application_id)
    new_status = request.POST.get('status')

    # Check if user is an employer and has permission to update this application
    if hasattr(request.user, 'profile') and request.user.profile.role == 'employer':
        # Check if the employer owns this job (more flexible matching)
        employer_company = request.user.profile.company_name or ""
        job_company = application.job.company or ""

        # Allow update if company names match (case-insensitive) or if employer company is empty
        if (employer_company.lower() in job_company.lower() or
            job_company.lower() in employer_company.lower() or
            not employer_company.strip()):
            if new_status in dict(Application.STATUS_CHOICES):
                application.status = new_status
                application.save()
                messages.success(request, f'Application status updated to {application.get_status_display()}')
            else:
                messages.error(request, 'Invalid status')
        else:
            messages.error(request, 'You do not have permission to update this application')
    else:
        messages.error(request, 'Only employers can update application status')

    return redirect('dashboard')


@login_required
def interview_results(request, session_id):
    """View detailed interview results"""
    session = get_object_or_404(InterviewSession, id=session_id, candidate=request.user)

    if session.status != 'completed':
        return redirect('interview_session', session_id=session_id)

    from .utils import InterviewEngine
    engine = InterviewEngine(session)
    final_score = engine.calculate_final_score()
    skill_breakdown = engine.get_skill_breakdown()

    # Calculate percentages for progress bars (score out of 5, convert to percentage)
    skill_breakdown_percentages = {skill: (score / 5) * 100 for skill, score in skill_breakdown.items()}
    
    # Create combined skill data for easier template access
    skill_data = [
        {'name': skill, 'score': score, 'percentage': skill_breakdown_percentages[skill]}
        for skill, score in skill_breakdown.items()
    ]

    context = {
        'session': session,
        'final_score': final_score,
        'skill_breakdown': skill_breakdown,
        'skill_data': skill_data,
        'responses': InterviewResponse.objects.filter(interview_session=session).select_related('question'),
    }
    return render(request, 'jobs/interview_results.html', context)