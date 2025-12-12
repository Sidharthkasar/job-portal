from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_map_page, name='skill_map'),  # page
    path('api/create/', views.create_skill_map, name='create_skill_map'),  # API
]
