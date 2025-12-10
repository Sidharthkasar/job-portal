from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def employer_dashboard(request):
    return HttpResponse("Employer Dashboard Working!")