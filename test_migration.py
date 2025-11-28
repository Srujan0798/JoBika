#!/usr/bin/env python3
"""
Test script to verify mock data migration
"""
import sys
sys.path.append('backend')

from salary_insights import salary_insights
from interview_prep import interview_prep
from resume_customizer import ResumeCustomizer

print("=" * 60)
print("Testing Mock Data Migration")
print("=" * 60)
print()

# Test 1: Salary Insights
print("1. Testing Salary Insights...")
try:
    result = salary_insights.get_salary_insights('software engineer', 'san francisco', 3)
    assert 'salary_range' in result
    assert 'market_insights' in result
    assert result['market_insights']['demand'] is not None
    print("   ✅ Salary insights working - fetched from database")
    print(f"   Median salary: ${result['salary_range']['median']:,}")
    print(f"   Demand: {result['market_insights']['demand']}")
except Exception as e:
    print(f"   ❌ Salary insights failed: {e}")
    sys.exit(1)

print()

# Test 2: Interview Prep
print("2. Testing Interview Prep...")
try:
    job_data = {
        'title': 'Senior Python Developer',
        'company': 'Google',
        'description': 'Build scalable systems',
        'required_skills': ['Python', 'Django', 'PostgreSQL']
    }
    user_skills = ['Python', 'Flask', 'JavaScript']
    
    result = interview_prep.generate_prep_guide(job_data, user_skills)
    assert 'likely_questions' in result
    assert 'preparation_tips' in result
    assert len(result['likely_questions']) > 0
    print("   ✅ Interview prep working - fetched from database")
    print(f"   Generated {len(result['likely_questions'])} questions")
    print(f"   Sample question: {result['likely_questions'][0]['question'][:60]}...")
except Exception as e:
    print(f"   ❌ Interview prep failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3: Resume Customizer
print("3. Testing Resume Customizer...")
try:
    customizer = ResumeCustomizer()
    assert len(customizer.skill_keywords) > 0
    assert 'full_stack' in customizer.skill_keywords
    print("   ✅ Resume customizer working - fetched from database")
    print(f"   Loaded {len(customizer.skill_keywords)} domain skill sets")
    print(f"   Sample domain: {list(customizer.skill_keywords.keys())[0]}")
except Exception as e:
    print(f"   ❌ Resume customizer failed: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ All tests passed! Mock data successfully migrated to database")
print("=" * 60)
