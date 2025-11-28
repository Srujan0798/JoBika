"""
Interview Preparation Tips for JoBika
AI-powered interview tips based on job and resume
"""

import json
import random
from database import get_db_connection, get_placeholder

class InterviewPrepSystem:
    """Generate interview preparation tips"""
    
    def __init__(self):
        pass  # No more hardcoded data
    
    def _get_questions_by_category(self, category):
        """Get interview questions from database by category"""
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        cursor.execute(f'SELECT question_template, tip FROM interview_questions WHERE category = {P}', (category,))
        questions = cursor.fetchall()
        conn.close()
        
        return questions
    
    def _get_tips_by_stage(self, stage):
        """Get interview tips from database by stage"""
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        cursor.execute(f'SELECT tip_text FROM interview_tips WHERE stage = {P}', (stage,))
        tips = cursor.fetchall()
        conn.close()
        
        return [t['tip_text'] if isinstance(t, dict) else t[0] for t in tips]
    
    def generate_prep_guide(self, job_data, user_skills):
        """
        Generate comprehensive interview prep guide
        
        Args:
            job_data: dict with title, company, description, required_skills
            user_skills: list of user's skills
        
        Returns:
            dict with questions, tips, and resources
        """
        job_title = job_data.get('title', 'this position')
        company = job_data.get('company', 'the company')
        required_skills = job_data.get('required_skills', [])
        
        # Match skills
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        matching_skills = list(set(user_skills_lower) & set(required_skills_lower))
        missing_skills = list(set(required_skills_lower) - set(user_skills_lower))
        
        # Generate questions
        questions = self._generate_questions(
            job_title, company, matching_skills, missing_skills
        )
        
        # Get tips from database
        prep_tips = self._get_tips_by_stage('preparation')
        during_tips = self._get_tips_by_stage('during')
        after_tips = self._get_tips_by_stage('after')
        
        tips = {
            'preparation': random.sample(prep_tips, min(3, len(prep_tips))) if prep_tips else [],
            'during': random.sample(during_tips, min(3, len(during_tips))) if during_tips else [],
            'after': random.sample(after_tips, min(3, len(after_tips))) if after_tips else []
        }
        
        # Areas to focus
        focus_areas = []
        if matching_skills:
            focus_areas.append({
                'area': 'Technical Skills',
                'description': f"Be ready to discuss your experience with: {', '.join(matching_skills[:5])}"
            })
        
        if missing_skills:
            focus_areas.append({
                'area': 'Skill Gaps',
                'description': f"Explain how you'd learn: {', '.join(missing_skills[:3])}"
            })
        
        focus_areas.append({
            'area': 'Company Knowledge',
            'description': f"Research {company}'s recent news, products, and culture"
        })
        
        return {
            'job_info': {
                'title': job_title,
                'company': company
            },
            'likely_questions': questions,
            'preparation_tips': tips,
            'focus_areas': focus_areas,
            'skill_match': {
                'matching': matching_skills,
                'to_learn': missing_skills[:5]
            }
        }
    
    def _generate_questions(self, job_title, company, matching_skills, missing_skills):
        """Generate likely interview questions from database"""
        questions = []
        
        # Technical questions based on matching skills
        tech_questions = self._get_questions_by_category('technical')
        for skill in matching_skills[:5]:
            if tech_questions:
                q = random.choice(tech_questions)
                template = q['question_template'] if isinstance(q, dict) else q[0]
                tip = q['tip'] if isinstance(q, dict) else q[1]
                questions.append({
                    'type': 'technical',
                    'question': template.format(skill=skill.title()),
                    'tip': tip or f"Prepare a specific example of using {skill.title()} in a project"
                })
        
        # Questions about missing skills
        for skill in missing_skills[:2]:
            questions.append({
                'type': 'technical',
                'question': f"Are you familiar with {skill.title()}? How would you learn it?",
                'tip': "Be honest but show enthusiasm for learning"
            })
        
        # Behavioral questions
        behavioral_questions = self._get_questions_by_category('behavioral')
        for q in random.sample(behavioral_questions, min(3, len(behavioral_questions))):
            template = q['question_template'] if isinstance(q, dict) else q[0]
            tip = q['tip'] if isinstance(q, dict) else q[1]
            questions.append({
                'type': 'behavioral',
                'question': template,
                'tip': tip or "Use the STAR method (Situation, Task, Action, Result)"
            })
        
        # Company-specific questions
        company_questions = self._get_questions_by_category('company')
        for q in random.sample(company_questions, min(2, len(company_questions))):
            template = q['question_template'] if isinstance(q, dict) else q[0]
            tip = q['tip'] if isinstance(q, dict) else q[1]
            questions.append({
                'type': 'company',
                'question': template.format(company=company),
                'tip': tip or f"Research {company}'s mission, values, and recent news"
            })
        
        # Role-specific questions
        role_questions = self._get_questions_by_category('role_specific')
        for q in random.sample(role_questions, min(2, len(role_questions))):
            template = q['question_template'] if isinstance(q, dict) else q[0]
            tip = q['tip'] if isinstance(q, dict) else q[1]
            questions.append({
                'type': 'role',
                'question': template.format(role=job_title),
                'tip': tip or "Connect your experience to the job requirements"
            })
        
        return questions

# Global instance
interview_prep = InterviewPrepSystem()

def init_interview_prep_endpoints(app):
    """Initialize interview prep endpoints"""
    from flask import request, jsonify
    
    @app.route('/api/interview/prep', methods=['POST'])
    def get_interview_prep():
        """Get interview preparation guide"""
        from server import verify_token
        from database import get_db_connection, get_placeholder
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.json
        job_id = data.get('jobId')
        
        if not job_id:
            return jsonify({'error': 'Job ID required'}), 400
        
        # Get job data
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        cursor.execute(f'SELECT * FROM jobs WHERE id = {P}', (job_id,))
        job = cursor.fetchone()
        
        if not job:
            conn.close()
            return jsonify({'error': 'Job not found'}), 404
        
        # Get user's latest resume
        cursor.execute(f'''
            SELECT skills FROM resumes
            WHERE user_id = {P}
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        resume = cursor.fetchone()
        
        conn.close()
        
        user_skills = json.loads(resume['skills']) if resume and resume['skills'] else []
        
        job_data = {
            'title': job['title'],
            'company': job['company'],
            'description': job['description'],
            'required_skills': json.loads(job['required_skills']) if job['required_skills'] else []
        }
        
        # Generate prep guide
        prep_guide = interview_prep.generate_prep_guide(job_data, user_skills)
        
        return jsonify(prep_guide)
    
    print("✅ Interview prep endpoints initialized")
