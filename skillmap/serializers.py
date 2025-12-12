from rest_framework import serializers
from .models import CandidateSkillProfile

class CandidateSkillProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkillProfile
        fields = '__all__'