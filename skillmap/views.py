from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CandidateSkillProfile
from .serializers import CandidateSkillProfileSerializer
from .utils.github_extractor import extract_github_skills
from .utils.linkedin_extractor import extract_linkedin_skills
from .utils.resume_parser import extract_text_from_resume
from .utils.skill_extractor import extract_skills

# Render the Skill Map page
def skill_map_page(request):
    return render(request, "skillmap/skill_map.html")


# API to create skill map
@api_view(["POST"])
def create_skill_map(request):
    try:
        github_username = request.data.get("github_username")
        linkedin_username = request.data.get("linkedin_username")
        resume_file = request.FILES.get("resume")

        # 1. Resume parsing
        resume_text = extract_text_from_resume(resume_file) if resume_file else ""
        resume_skills = extract_skills(resume_text) if resume_text else []

        # 2. GitHub skills
        github_skills = extract_github_skills(github_username) if github_username else []

        # 3. LinkedIn skills
        linkedin_skills = extract_linkedin_skills(linkedin_username) if linkedin_username else []

        # 4. Combine all skills
        final_skill_map = list(set(resume_skills + github_skills + linkedin_skills))

        profile = CandidateSkillProfile.objects.create(
            github_username=github_username,
            linkedin_username=linkedin_username,
            resume_text=resume_text,
            extracted_skills=resume_skills,
            github_skills=github_skills,
            linkedin_skills=linkedin_skills,
            final_skill_map=final_skill_map,
        )

        serializer = CandidateSkillProfileSerializer(profile)
        return Response({"message": "Skill map created", "profile": serializer.data})

    except Exception as e:
        return Response({"error": str(e)}, status=400)
