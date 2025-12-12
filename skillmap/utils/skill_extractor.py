import re

def extract_skills(text):
    """
    Simple keyword extraction from text.
    Returns a list of skills found.
    """
    # Example skill keywords
    SKILLS_KEYWORDS = [
        "Python", "Django", "Flask", "React", "JavaScript", 
        "SQL", "Git", "REST", "HTML", "CSS", "Machine Learning"
    ]
    
    found_skills = []
    for skill in SKILLS_KEYWORDS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills
