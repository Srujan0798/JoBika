#!/usr/bin/env python3
"""
Seed database with data from hardcoded Python files
This replaces mock data with real database entries
"""
import json
from database import get_db_connection, get_placeholder

def seed_salary_data():
    """Seed salary roles and location multipliers"""
    print("🌱 Seeding salary data...")
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    P = get_placeholder(db_type)
    
    # Salary data from salary_insights.py
    salary_data = [
        ('software engineer', 80000, 180000, 120000, 'High', 'Stable', 'High', '["System Design", "AWS", "Kubernetes"]'),
        ('senior software engineer', 120000, 220000, 160000, 'High', 'Growing (↑ 8%)', 'High', '["System Design", "AWS", "Kubernetes"]'),
        ('data scientist', 90000, 190000, 130000, 'High', 'Growing (↑ 15%)', 'High', '["Deep Learning", "MLOps", "Python"]'),
        ('product manager', 100000, 200000, 140000, 'Medium', 'Stable', 'High', '["Cloud", "Agile", "Leadership"]'),
        ('frontend developer', 70000, 150000, 100000, 'Medium', 'Stable', 'Medium', '["React", "TypeScript", "Next.js"]'),
        ('backend developer', 80000, 170000, 115000, 'High', 'Stable', 'High', '["Microservices", "Docker", "PostgreSQL"]'),
        ('full stack developer', 85000, 175000, 120000, 'High', 'Growing (↑ 8%)', 'High', '["System Design", "AWS", "Kubernetes"]'),
        ('devops engineer', 90000, 180000, 125000, 'High', 'Growing (↑ 15%)', 'High', '["Cloud", "Agile", "Leadership"]'),
        ('machine learning engineer', 100000, 210000, 145000, 'High', 'Growing (↑ 15%)', 'High', '["Deep Learning", "MLOps", "Python"]'),
        ('ui ux designer', 65000, 140000, 95000, 'Medium', 'Stable', 'Medium', '["Cloud", "Agile", "Leadership"]'),
        ('qa engineer', 60000, 130000, 85000, 'Medium', 'Stable', 'Medium', '["Cloud", "Agile", "Leadership"]'),
    ]
    
    for role_name, min_sal, max_sal, median_sal, demand, growth, competition, skills in salary_data:
        cursor.execute(f'''
            INSERT INTO salary_roles (role_name, min_salary, max_salary, median_salary, demand_level, growth_trend, competition_level, top_skills)
            VALUES ({P}, {P}, {P}, {P}, {P}, {P}, {P}, {P})
            ON CONFLICT (role_name) DO NOTHING
        ''', (role_name, min_sal, max_sal, median_sal, demand, growth, competition, skills))
    
    # Location multipliers
    location_data = [
        ('san francisco', 1.4),
        ('new york', 1.3),
        ('seattle', 1.25),
        ('boston', 1.2),
        ('austin', 1.1),
        ('remote', 1.0),
        ('bangalore', 0.3),
        ('london', 1.25),
    ]
    
    for location, multiplier in location_data:
        cursor.execute(f'''
            INSERT INTO location_multipliers (location_name, multiplier)
            VALUES ({P}, {P})
            ON CONFLICT (location_name) DO NOTHING
        ''', (location, multiplier))
    
    conn.commit()
    print(f"✅ Seeded {len(salary_data)} salary roles and {len(location_data)} locations")

def seed_interview_data():
    """Seed interview questions and tips"""
    print("🌱 Seeding interview data...")
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    P = get_placeholder(db_type)
    
    # Technical questions
    technical_questions = [
        "Explain your experience with {skill}",
        "How would you approach a problem involving {skill}?",
        "What is your proficiency level with {skill}?",
        "Can you walk me through a project where you used {skill}?",
        "What are the pros and cons of {skill} compared to alternatives?",
    ]
    
    for q in technical_questions:
        cursor.execute(f'''
            INSERT INTO interview_questions (category, question_template, tip)
            VALUES ({P}, {P}, {P})
        ''', ('technical', q, 'Prepare a specific example of using this skill in a project'))
    
    # Behavioral questions
    behavioral_questions = [
        "Tell me about a time when you faced a challenging project",
        "How do you handle tight deadlines?",
        "Describe a situation where you had to work with a difficult team member",
        "What is your greatest professional achievement?",
        "How do you stay updated with industry trends?",
        "Describe a failure and what you learned from it",
    ]
    
    for q in behavioral_questions:
        cursor.execute(f'''
            INSERT INTO interview_questions (category, question_template, tip)
            VALUES ({P}, {P}, {P})
        ''', ('behavioral', q, 'Use the STAR method (Situation, Task, Action, Result)'))
    
    # Company questions
    company_questions = [
        "Why do you want to work at {company}?",
        "What do you know about {company}'s products/services?",
        "How do you align with {company}'s values?",
        "Where do you see yourself in 5 years at {company}?",
    ]
    
    for q in company_questions:
        cursor.execute(f'''
            INSERT INTO interview_questions (category, question_template, tip)
            VALUES ({P}, {P}, {P})
        ''', ('company', q, "Research the company's mission, values, and recent news"))
    
    # Role-specific questions
    role_questions = [
        "Why are you interested in the {role} position?",
        "What makes you a good fit for {role}?",
        "What challenges do you anticipate in this {role}?",
        "How would you contribute to our team as a {role}?",
    ]
    
    for q in role_questions:
        cursor.execute(f'''
            INSERT INTO interview_questions (category, question_template, tip)
            VALUES ({P}, {P}, {P})
        ''', ('role_specific', q, 'Connect your experience to the job requirements'))
    
    # Interview tips
    tips_data = [
        ('preparation', 'Research the company thoroughly before the interview'),
        ('preparation', 'Practice your answers using the STAR method (Situation, Task, Action, Result)'),
        ('preparation', 'Prepare questions to ask the interviewer'),
        ('preparation', 'Review your resume and be ready to discuss each point'),
        ('preparation', 'Test your tech setup if it\'s a virtual interview'),
        ('during', 'Arrive 10-15 minutes early (or join virtual meeting early)'),
        ('during', 'Make eye contact and show enthusiasm'),
        ('during', 'Listen carefully to questions before answering'),
        ('during', 'Use specific examples from your experience'),
        ('during', 'It\'s okay to ask for clarification if you don\'t understand a question'),
        ('after', 'Send a thank-you email within 24 hours'),
        ('after', 'Reflect on questions you found challenging'),
        ('after', 'Follow up on any action items mentioned'),
        ('after', 'Stay patient while waiting for a response'),
        ('after', 'Keep applying to other positions meanwhile'),
    ]
    
    for stage, tip in tips_data:
        cursor.execute(f'''
            INSERT INTO interview_tips (stage, tip_text)
            VALUES ({P}, {P})
        ''', (stage, tip))
    
    conn.commit()
    print(f"✅ Seeded {len(technical_questions) + len(behavioral_questions) + len(company_questions) + len(role_questions)} questions and {len(tips_data)} tips")

def seed_domain_skills():
    """Seed domain skills for resume customization"""
    print("🌱 Seeding domain skills...")
    
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    P = get_placeholder(db_type)
    
    domain_data = [
        ('full_stack', '["react", "node.js", "javascript", "typescript", "mongodb", "express", "vue", "angular"]'),
        ('backend', '["python", "java", "spring boot", "django", "flask", "microservices", "rest api", "graphql"]'),
        ('frontend', '["react", "vue", "angular", "html", "css", "javascript", "typescript", "tailwind"]'),
        ('ai_ml', '["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "computer vision"]'),
        ('data', '["python", "sql", "pandas", "numpy", "data analysis", "tableau", "power bi", "spark"]'),
        ('devops', '["docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", "terraform", "ansible"]'),
        ('mobile', '["react native", "flutter", "android", "ios", "swift", "kotlin", "java"]'),
    ]
    
    for domain, skills in domain_data:
        cursor.execute(f'''
            INSERT INTO domain_skills (domain_name, skills_list)
            VALUES ({P}, {P})
            ON CONFLICT (domain_name) DO NOTHING
        ''', (domain, skills))
    
    conn.commit()
    print(f"✅ Seeded {len(domain_data)} domain skill sets")

def main():
    """Run all seed functions"""
    print("=" * 60)
    print("JoBika Database Seeding")
    print("=" * 60)
    print()
    
    try:
        seed_salary_data()
        seed_interview_data()
        seed_domain_skills()
        
        print()
        print("=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
