from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
      path("dashboard/", views.dashboard_view, name="dashboard"), 
]
