from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # profile will be created by signals; update role afterwards
            user.profile.role = self.cleaned_data['role']
            user.profile.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('resume', 'skills')

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('company_name', 'company_website', 'contact_phone')
