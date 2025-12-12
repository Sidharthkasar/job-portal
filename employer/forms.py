# In employer/forms.py
from django import forms
from .models import Employer

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'contact_email', 'contact_phone', 'address']
