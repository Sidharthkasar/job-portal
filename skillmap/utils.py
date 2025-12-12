# skillmap/utils.py

import PyPDF2
import docx
import requests

def extract_text_from_resume(file):
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def fetch_github_languages(username):
    url = f"https://api.github.com/users/{username}/repos"
    r = requests.get(url)
    repos = r.json()
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    return list(languages.keys())

def extract_skills(text):
    common_skills = ["python", "django", "java", "javascript", "react", "sql", "html", "css"]
    found_skills = []
    text = text.lower()
    for skill in common_skills:
        if skill in text:
            found_skills.append(skill)
    return found_skills
