Core Framework, Tech Stack & Architecture
🔹 Core Framework & Backend

Python: Primary programming language

Django 6.0: Core web framework handling routing, views, models, authentication, and admin interface

Django REST Framework 3.16.1: RESTful APIs for job listings, user management, applications, and integrations

SQLite: Default development database (configured in settings.py)

🎨 Frontend & Templates

Django Templates: Server-side HTML rendering

Bootstrap 5: Consistent UI styling across all modules

(No separate frontend framework like React or Vue is used)

🧩 Additional Django Libraries & Tools

django-cors-headers: Handles Cross-Origin Resource Sharing (CORS)

django-widget-tweaks: Customizes Django form rendering

🤖 Data Processing & Machine Learning

Pandas 2.3.3: Data manipulation and analysis

NumPy 2.3.5: Numerical computing

Scikit-learn 1.8.0: Machine learning algorithms (used in Skill Mapping & matching logic)

SciPy 1.16.3: Scientific computing support

📄 Document & Media Handling

PyPDF2 3.0.1: PDF parsing (resume uploads)

python-docx 1.2.0: Microsoft Word document processing

Pillow (PIL) 12.0.0: Image handling and processing

🌐 Web Scraping & HTTP Utilities

Requests 2.32.5: HTTP requests for external data fetching

BeautifulSoup4 4.14.3: HTML parsing

lxml 6.0.2: Fast XML/HTML processing

🗂️ Project Structure

Custom Django Apps:

accounts – Authentication & user roles (Candidate / Employer)

jobs – Job listings & applications

employer – Employer dashboards & hiring actions

skillmap – Resume analysis & skill matching logic

resumes – Resume upload & processing

Standard Django Layout: Migrations, templates, static files

Virtual Environment: Managed via pyvenv.cfg and Scripts/



# 🚀 All-in-One Job Portal & Interview Platform (Django)

A **unified recruitment platform** built with Django that combines **job posting, candidate management, skill mapping, hiring funnel automation, and adaptive interviews** — all under a single login and interface.

This project is designed to run **locally without any external services or API keys**, making it ideal for learning, demos, and portfolio use.

---

## 🔗 Unified Navigation & Access

- **Single Entry Point:**  
  👉 http://127.0.0.1:8000/

- **Role-Based Navigation:**  
  - Candidates see candidate-specific dashboards and features  
  - Employers see employer-specific job and application management menus

- **Integrated URLs:**  
  All features are accessible from one domain with seamless navigation.

---

## 👥 User Journey – Complete Workflow

### 🧑‍💻 Candidate Workflow

1. **Register / Login**  
   👉 http://127.0.0.1:8000/accounts/register/

2. **Complete Profile**  
   - Upload Resume  
   - Add GitHub & LinkedIn links

3. **Skill Mapping**  
   👉 http://127.0.0.1:8000/skillmap/  
   (Integrated into the candidate dashboard)

4. **Browse Jobs**  
   👉 http://127.0.0.1:8000/

5. **Apply to Jobs**  
   - Apply directly from job listings

6. **Track Applications**  
   👉 http://127.0.0.1:8000/accounts/candidate/dashboard/

7. **Take Interviews**  
   - Automatic interview sessions triggered by status changes

8. **View Results**  
   - Detailed performance and skill analysis

---

### 🏢 Employer Workflow

1. **Register / Login**  
   👉 http://127.0.0.1:8000/accounts/register/

2. **Post Jobs**  
   👉 http://127.0.0.1:8000/create/

3. **Manage Applications**  
   👉 http://127.0.0.1:8000/employer/

4. **Update Candidate Status**  
   - Move candidates through the hiring funnel

5. **Start Interviews**  
   - Trigger adaptive interviews for candidates

6. **View Results**  
   - Access detailed candidate performance data

---

## 🔄 Feature Integration Points

### 1️⃣ Skill Mapping ↔ Job Portal
- Skills extracted from:
  - Resume
  - GitHub
  - LinkedIn
- Used for:
  - Interview question selection
  - Candidate dashboard insights

---

### 2️⃣ Job Portal ↔ Hiring Funnel
- Applications automatically enter the hiring pipeline
- Status updates trigger the next hiring stage
- Interview initiation directly from application management

---

### 3️⃣ Hiring Funnel ↔ Interview Engine
- Interview sessions triggered by funnel status
- Interview results update application status
- Performance data supports hiring decisions

---

### 4️⃣ Interview Engine ↔ Skill Mapping
- Questions selected based on candidate skill profile
- Adaptive difficulty based on performance
- Skill profiles updated after interviews

---

## 📱 Single Platform Architecture

### 🎯 Key Integration Features

- **Unified Database:**  
  All data stored in a single SQLite database

- **Shared User System:**  
  One login system for candidates and employers

- **Consistent UI:**  
  Bootstrap 5 used across all modules

- **Role-Based Access Control:**  
  Features are accessible based on user type

- **Seamless Navigation:**  
  Smooth movement between modules

- **Automated Data Flow:**  
  Skills → Jobs → Applications → Interviews

---

## 🚀 How to Run the Project

### 1️⃣ Start the Server
```bash
python manage.py runserver
