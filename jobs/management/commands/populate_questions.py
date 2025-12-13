from django.core.management.base import BaseCommand
from jobs.models import InterviewQuestion

class Command(BaseCommand):
    help = 'Populate database with sample interview questions'

    def handle(self, *args, **options):
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
            {
                'question_text': 'What is version control and why is it important?',
                'skill': 'git',
                'difficulty': 'easy',
                'expected_answer': 'Version control tracks changes to code over time. Important for collaboration, backup, and tracking project history.'
            },
            {
                'question_text': 'Explain the concept of responsive web design.',
                'skill': 'javascript',
                'difficulty': 'medium',
                'expected_answer': 'Responsive design makes websites adapt to different screen sizes using CSS media queries, flexible layouts, and responsive images.'
            },
            {
                'question_text': 'How would you optimize a slow database query?',
                'skill': 'sql',
                'difficulty': 'hard',
                'expected_answer': 'Check execution plan, add indexes, optimize joins, limit results, use proper data types, consider query restructuring.'
            },
            {
                'question_text': 'Describe a challenging project you worked on and how you overcame difficulties.',
                'skill': 'leadership',
                'difficulty': 'medium',
                'expected_answer': 'Should describe a specific project, challenges faced, solutions implemented, and lessons learned.'
            },
            {
                'question_text': 'How do you stay updated with new technologies and industry trends?',
                'skill': 'teamwork',
                'difficulty': 'easy',
                'expected_answer': 'Follow tech blogs, attend conferences, participate in online communities, take courses, work on personal projects.'
            },
        ]

        created_count = 0
        for q_data in questions_data:
            question, created = InterviewQuestion.objects.get_or_create(
                question_text=q_data['question_text'],
                defaults=q_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} interview questions')
        )