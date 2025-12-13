import random
from django.db import models
from django.db.models import Count
from .models import InterviewQuestion, InterviewSession, InterviewResponse

class InterviewEngine:
    """
    Adaptive interview question system that selects questions based on:
    1. Job requirements
    2. Candidate's skill profile
    3. Previous responses
    """

    def __init__(self, session):
        self.session = session
        self.candidate = session.candidate
        self.job = session.job_application.job

    def get_next_question(self):
        """
        Select the next question based on adaptive logic
        """
        # Get candidate's skills from profile
        candidate_skills = []
        if hasattr(self.candidate, 'profile') and self.candidate.profile.skills:
            candidate_skills = self.candidate.profile.skills

        # Extract skills from job description
        job_skills = self._extract_job_skills()

        # Get questions already asked
        asked_questions = self.session.questions_asked.all()
        asked_skills = asked_questions.values_list('skill', flat=True)

        # Priority 1: Skills mentioned in job description that candidate has
        priority_skills = set(job_skills) & set(candidate_skills)
        if priority_skills:
            available_questions = InterviewQuestion.objects.filter(
                skill__in=priority_skills
            ).exclude(id__in=asked_questions.values_list('id', flat=True))
        else:
            # Priority 2: Job skills (even if candidate doesn't have them)
            available_questions = InterviewQuestion.objects.filter(
                skill__in=job_skills
            ).exclude(id__in=asked_questions.values_list('id', flat=True))

        if not available_questions.exists():
            # Priority 3: General questions not asked yet
            available_questions = InterviewQuestion.objects.exclude(
                id__in=asked_questions.values_list('id', flat=True)
            )

        if available_questions.exists():
            # Select question with appropriate difficulty
            return self._select_by_difficulty(available_questions)
        else:
            # If all questions asked, return random question (allow repeats in advanced mode)
            return InterviewQuestion.objects.order_by('?').first()

    def _extract_job_skills(self):
        """
        Extract skills from job description (simple keyword matching)
        """
        job_text = f"{self.job.title} {self.job.description}".lower()
        skill_keywords = {
            'python': ['python', 'django', 'flask', 'fastapi'],
            'javascript': ['javascript', 'js', 'react', 'vue', 'angular', 'node'],
            'sql': ['sql', 'database', 'mysql', 'postgresql', 'mongodb'],
            'git': ['git', 'github', 'version control'],
            'problem_solving': ['problem solving', 'algorithms', 'debugging'],
            'communication': ['communication', 'presentation', 'teamwork'],
        }

        found_skills = []
        for skill, keywords in skill_keywords.items():
            if any(keyword in job_text for keyword in keywords):
                found_skills.append(skill)

        return found_skills or ['problem_solving', 'communication']  # Default skills

    def _select_by_difficulty(self, questions):
        """
        Select question based on candidate's performance so far
        """
        responses = InterviewResponse.objects.filter(interview_session=self.session)

        if not responses.exists():
            # First question - start with medium difficulty
            return questions.filter(difficulty='medium').order_by('?').first() or questions.order_by('?').first()

        avg_score = responses.aggregate(avg=models.Avg('score')).get('avg') or 3

        if avg_score >= 4:
            # Doing well - increase difficulty
            return (questions.filter(difficulty='hard').order_by('?').first() or
                   questions.filter(difficulty='medium').order_by('?').first() or
                   questions.order_by('?').first())
        elif avg_score <= 2:
            # Struggling - decrease difficulty
            return (questions.filter(difficulty='easy').order_by('?').first() or
                   questions.filter(difficulty='medium').order_by('?').first() or
                   questions.order_by('?').first())
        else:
            # Medium performance - keep medium difficulty
            return questions.filter(difficulty='medium').order_by('?').first() or questions.order_by('?').first()

    def calculate_final_score(self):
        """
        Calculate overall interview score
        """
        responses = InterviewResponse.objects.filter(interview_session=self.session)
        if not responses.exists():
            return 0

        total_score = sum(response.score for response in responses)
        max_possible = len(responses) * 5  # Assuming 5-point scale
        return (total_score / max_possible) * 100 if max_possible > 0 else 0

    def get_skill_breakdown(self):
        """
        Get performance breakdown by skill
        """
        responses = InterviewResponse.objects.filter(
            interview_session=self.session
        ).select_related('question')

        skill_scores = {}
        for response in responses:
            skill = response.question.skill
            if skill not in skill_scores:
                skill_scores[skill] = []
            skill_scores[skill].append(response.score)

        # Calculate average for each skill
        breakdown = {}
        for skill, scores in skill_scores.items():
            breakdown[skill] = sum(scores) / len(scores) if scores else 0

        return breakdown


def create_sample_questions():
    """
    Create sample interview questions for testing
    """
    questions_data = [
        {
            'question_text': 'Explain what a variable is in Python and give an example.',
            'skill': 'python',
            'difficulty': 'easy',
            'expected_answer': 'A variable is a container for storing data values. Example: x = 5'
        },
        {
            'question_text': 'What is the difference between a list and a tuple in Python?',
            'skill': 'python',
            'difficulty': 'medium',
            'expected_answer': 'Lists are mutable (can be changed), tuples are immutable (cannot be changed).'
        },
        {
            'question_text': 'Explain Django\'s MTV architecture.',
            'skill': 'django',
            'difficulty': 'medium',
            'expected_answer': 'Model-Template-View: Model handles data, Template handles presentation, View handles logic.'
        },
        {
            'question_text': 'What is the purpose of React\'s useState hook?',
            'skill': 'react',
            'difficulty': 'medium',
            'expected_answer': 'useState allows functional components to have state variables.'
        },
        {
            'question_text': 'Write a SQL query to find employees with salary > 50000.',
            'skill': 'sql',
            'difficulty': 'easy',
            'expected_answer': 'SELECT * FROM employees WHERE salary > 50000;'
        },
        {
            'question_text': 'Describe how you would approach solving a complex coding problem.',
            'skill': 'problem_solving',
            'difficulty': 'medium',
            'expected_answer': 'Break down the problem, identify inputs/outputs, consider edge cases, write pseudocode, implement and test.'
        },
        {
            'question_text': 'How do you handle conflicts within a development team?',
            'skill': 'communication',
            'difficulty': 'medium',
            'expected_answer': 'Listen to all sides, find common ground, focus on solutions, involve mediator if needed.'
        },
    ]

    for q_data in questions_data:
        InterviewQuestion.objects.get_or_create(
            question_text=q_data['question_text'],
            defaults=q_data
        )