import requests

def fetch_github_languages(username):
    """
    Fetch GitHub repository languages for a given username.
    Returns a list of languages.
    """
    if not username:
        return []
    
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    repos = response.json()
    languages = set()
    for repo in repos:
        lang = repo.get('language')
        if lang:
            languages.add(lang)
    return list(languages)

