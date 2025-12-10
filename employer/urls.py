from django.urls import path
from . import views

urlpatterns = [
    path('', views.employer_dashboard, name='employer_dashboard'),
]
