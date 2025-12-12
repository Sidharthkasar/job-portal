import requests


def extract_github_skills(username, token=None):
    """
    Extract skills from GitHub profile and repositories
    """
    skills = []
    languages = []
    
    if not username:
        return []
    
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        # 1. Get user profile
        profile_url = f"https://api.github.com/users/{username}"
        profile_response = requests.get(profile_url, headers=headers)
        
        if profile_response.status_code != 200:
            return []
        
        # 2. Get user repositories
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        repos_response = requests.get(repos_url, headers=headers)
        
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            
            # Extract programming languages from repos
            for repo in repos_data:
                if repo.get('language'):
                    languages.append(repo['language'].lower())
                
                # Check description for skills
                description = repo.get('description', '').lower()
                skills_from_desc = extract_skills_from_text(description)
                skills.extend(skills_from_desc)
        
        # 3. Get pinned repositories (if any)
        pinned_query = """
        query($username: String!) {
            user(login: $username) {
                pinnedItems(first: 6, types: REPOSITORY) {
                    nodes {
                        ... on Repository {
                            name
                            description
                            primaryLanguage {
                                name
                            }
                        }
                    }
                }
            }
        }
        """
        
        # Try GraphQL API if token is available
        if token:
            graphql_url = "https://api.github.com/graphql"
            graphql_response = requests.post(
                graphql_url,
                json={'query': pinned_query, 'variables': {'username': username}},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if graphql_response.status_code == 200:
                pinned_data = graphql_response.json()
                if 'data' in pinned_data and pinned_data['data']['user']:
                    for repo in pinned_data['data']['user']['pinnedItems']['nodes']:
                        if repo.get('primaryLanguage'):
                            languages.append(repo['primaryLanguage']['name'].lower())
        
        # 4. Combine and deduplicate
        all_skills = list(set(skills + languages))
        
        # 5. Map languages to common skill names
        skill_mapping = {
            'python': ['python', 'django', 'flask', 'fastapi'],
            'javascript': ['javascript', 'node.js', 'express', 'react', 'vue', 'angular'],
            'java': ['java', 'spring', 'hibernate'],
            'c#': ['c#', '.net', 'asp.net'],
            'php': ['php', 'laravel', 'symfony'],
            'ruby': ['ruby', 'rails'],
            'go': ['go', 'golang'],
            'rust': ['rust'],
            'swift': ['swift'],
            'kotlin': ['kotlin'],
        }
        
        final_skills = []
        for skill in all_skills:
            skill_lower = skill.lower()
            # Check if skill matches any in mapping
            for main_skill, aliases in skill_mapping.items():
                if skill_lower in aliases or any(alias in skill_lower for alias in aliases):
                    if main_skill not in final_skills:
                        final_skills.append(main_skill)
                    break
            else:
                if skill_lower not in final_skills:
                    final_skills.append(skill_lower)
        
        return final_skills[:20]  # Return top 20 skills
        
    except Exception as e:
        print(f"GitHub API Error: {e}")
        return []

def extract_skills_from_text(text):
    """
    Extract technical skills from text
    """
    common_skills = [
        'python', 'django', 'flask', 'fastapi',
        'javascript', 'react', 'vue', 'angular', 'node.js', 'express',
        'java', 'spring', 'hibernate',
        'c#', '.net', 'asp.net',
        'php', 'laravel', 'symfony',
        'ruby', 'rails',
        'go', 'golang',
        'rust',
        'swift',
        'kotlin',
        'sql', 'mysql', 'postgresql', 'mongodb',
        'docker', 'kubernetes',
        'aws', 'azure', 'gcp',
        'git', 'github', 'gitlab',
        'html', 'css', 'sass', 'less',
        'typescript',
        'rest', 'graphql',
        'redis', 'rabbitmq',
        'linux', 'unix',
        'agile', 'scrum',
        'ci/cd', 'jenkins',
        'machine learning', 'ai', 'data science'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills