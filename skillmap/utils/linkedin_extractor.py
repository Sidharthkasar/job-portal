import requests
from django.conf import settings

def extract_linkedin_skills(username=None, access_token=None):
    """
    Extract skills from LinkedIn profile
    Note: LinkedIn API requires OAuth2 authentication
    """
    skills = []
    
    # Method 1: If we have access token (for authenticated users)
    if access_token:
        try:
            # LinkedIn API endpoints
            profile_url = "https://api.linkedin.com/v2/me"
            skills_url = "https://api.linkedin.com/v2/skills"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            # Get profile to get person URN
            profile_response = requests.get(profile_url, headers=headers)
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                person_urn = profile_data.get('id')
                
                # Get skills using person URN
                if person_urn:
                    skills_response = requests.get(
                        f"https://api.linkedin.com/v2/skills?q=members&member={person_urn}&count=100",
                        headers=headers
                    )
                    
                    if skills_response.status_code == 200:
                        skills_data = skills_response.json()
                        if 'elements' in skills_data:
                            for skill_item in skills_data['elements']:
                                if 'skill' in skill_item and 'name' in skill_item['skill']:
                                    skills.append(skill_item['skill']['name'].lower())
            
        except Exception as e:
            print(f"LinkedIn API Error: {e}")
    
    # Method 2: Web scraping fallback (requires legal compliance)
    elif username:
        # This is a placeholder - implement web scraping carefully
        # Ensure you comply with LinkedIn's terms of service
        skills = scrape_linkedin_skills_placeholder(username)
    
    # Map LinkedIn skills to standardized skill names
    return standardize_skills(skills)

def scrape_linkedin_skills_placeholder(username):
    """
    Placeholder function for LinkedIn web scraping
    In production, implement proper web scraping with consent
    """
    # This is just a placeholder - implement actual scraping
    # or use a service like ProxyCrawl or ScrapingBee
    
    # For now, return empty list
    return []

def standardize_skills(skills):
    """
    Standardize LinkedIn skill names to match our skill mapping
    """
    skill_mapping = {
        'python': ['python', 'django', 'flask', 'python programming'],
        'javascript': ['javascript', 'js', 'ecmascript', 'node.js', 'react.js', 'angular.js'],
        'java': ['java', 'java ee', 'spring framework', 'hibernate'],
        'c#': ['c#', 'c sharp', '.net', 'asp.net'],
        'php': ['php', 'laravel', 'codeigniter'],
        'html/css': ['html', 'css', 'html5', 'css3', 'front-end'],
        'sql': ['sql', 'mysql', 'postgresql', 'database'],
        'git': ['git', 'github', 'gitlab', 'version control'],
        'docker': ['docker', 'containerization'],
        'aws': ['aws', 'amazon web services', 'cloud computing'],
        'agile': ['agile', 'scrum', 'kanban'],
        'machine learning': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
    }
    
    standardized = []
    
    for skill in skills:
        skill_lower = skill.lower()
        mapped = False
        
        for standard_skill, variants in skill_mapping.items():
            if skill_lower in variants or any(variant in skill_lower for variant in variants):
                if standard_skill not in standardized:
                    standardized.append(standard_skill)
                mapped = True
                break
        
        if not mapped and skill_lower not in standardized:
            standardized.append(skill_lower)
    
    return standardized
