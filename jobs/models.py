from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('assessment', 'Assessment'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to user
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class InterviewQuestion(models.Model):
    SKILL_CHOICES = (
        ('python', 'Python'),
        ('django', 'Django'),
        ('javascript', 'JavaScript'),
        ('react', 'React'),
        ('sql', 'SQL'),
        ('git', 'Git'),
        ('problem_solving', 'Problem Solving'),
        ('communication', 'Communication'),
        ('teamwork', 'Teamwork'),
        ('leadership', 'Leadership'),
    )

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    question_text = models.TextField()
    skill = models.CharField(max_length=50, choices=SKILL_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    expected_answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill} - {self.question_text[:50]}"


class InterviewSession(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    job_application = models.ForeignKey('jobs.Application', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    current_skill_focus = models.CharField(max_length=50, blank=True, null=True)
    total_questions = models.IntegerField(default=5)
    questions_asked = models.ManyToManyField(InterviewQuestion, through='InterviewResponse')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.candidate.username} - {self.job_application.job.title}"


class InterviewResponse(models.Model):
    interview_session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    candidate_answer = models.TextField()
    score = models.IntegerField(default=0)  # 1-5 scale
    feedback = models.TextField(blank=True, null=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('interview_session', 'question')

    def __str__(self):
        return f"Response to {self.question.skill} question"
