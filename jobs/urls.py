from django.urls import path
from .views import job_list, job_detail, create_job

urlpatterns = [
    path('', job_list, name='job_list'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('create/', create_job, name='create_job'),
]
