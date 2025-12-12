from django.db import models

class CandidateSkillProfile(models.Model):
    github_username = models.CharField(max_length=100, blank=True, null=True)
    linkedin_username = models.CharField(max_length=100, blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)
    extracted_skills = models.JSONField(default=list)
    github_skills = models.JSONField(default=list)
    linkedin_skills = models.JSONField(default=list)
    final_skill_map = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.github_username or "Candidate Skill Profile"
