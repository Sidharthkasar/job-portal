from django.urls import path
from .views import job_list, job_detail, create_job, apply_job, dashboard

urlpatterns = [
    path("", job_list, name="job_list"),
    path("job/<int:job_id>/", job_detail, name="job_detail"),
    path("job/<int:job_id>/apply/", apply_job, name="apply_job"),
    path("create/", create_job, name="create_job"),
     path('dashboard/', dashboard, name='dashboard'),
]
