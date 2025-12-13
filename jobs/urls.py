from django.urls import path
from .views import (job_list, job_detail, create_job, apply_job, save_job, dashboard,
                   start_interview, interview_session, submit_answer, interview_results,
                   update_application_status)

urlpatterns = [
    path("", job_list, name="job_list"),
    path("job/<int:job_id>/", job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", apply_job, name="apply_job"),
    path("job/<int:job_id>/save/", save_job, name="save_job"),
    path("create/", create_job, name="create_job"),
    path('dashboard/', dashboard, name='dashboard'),
    # Interview URLs
    path('interview/start/<int:application_id>/', start_interview, name='start_interview'),
    path('interview/session/<int:session_id>/', interview_session, name='interview_session'),
    path('interview/submit/<int:session_id>/', submit_answer, name='submit_answer'),
    path('interview/results/<int:session_id>/', interview_results, name='interview_results'),
    # Application management
    path('application/<int:application_id>/update-status/', update_application_status, name='update_application_status'),
]
