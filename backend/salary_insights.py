"""
Salary Insights API for JoBika
Provides salary data and market insights for job positions
"""

import json
from datetime import datetime
from database import get_db_connection, get_placeholder

class SalaryInsightsSystem:
    """Generate salary insights and market data"""
    
    def __init__(self):
        pass  # No more hardcoded data
    
    def _get_salary_role(self, job_title):
        """Get salary data from database for a role"""
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        # Normalize title
        title_lower = job_title.lower()
        
        # Try exact match first
        cursor.execute(f'SELECT * FROM salary_roles WHERE role_name = {P}', (title_lower,))
        role = cursor.fetchone()
        
        # If no exact match, try partial match
        if not role:
            cursor.execute(f'SELECT * FROM salary_roles WHERE {P} LIKE \'%\' || role_name || \'%\'', (title_lower,))
            role = cursor.fetchone()
        
        # If still no match, get default software engineer
        if not role:
            cursor.execute(f'SELECT * FROM salary_roles WHERE role_name = {P}', ('software engineer',))
            role = cursor.fetchone()
        
        conn.close()
        return role
    
    def _get_location_multiplier(self, location):
        """Get location multiplier from database"""
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        location_lower = location.lower()
        
        # Try exact match
        cursor.execute(f'SELECT multiplier FROM location_multipliers WHERE location_name = {P}', (location_lower,))
        result = cursor.fetchone()
        
        # If no match, try partial match
        if not result:
            cursor.execute(f'SELECT multiplier FROM location_multipliers WHERE {P} LIKE \'%\' || location_name || \'%\' LIMIT 1', (location_lower,))
            result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result['multiplier'] if isinstance(result, dict) else result[0]
        return 1.0  # default
    
    def get_salary_insights(self, job_title, location='remote', experience_years=2):
        """
        Get salary insights for a job
        
        Args:
            job_title: Job position title
            location: Job location
            experience_years: Years of experience
        
        Returns:
            dict with salary insights
        """
        # Get salary role from database
        role = self._get_salary_role(job_title)
        
        if not role:
            return {
                'error': 'No salary data found for this role',
                'job_title': job_title
            }
        
        # Get base salary range
        base_min = role['min_salary'] if isinstance(role, dict) else role[2]
        base_max = role['max_salary'] if isinstance(role, dict) else role[3]
        base_median = role['median_salary'] if isinstance(role, dict) else role[4]
        
        # Apply location multiplier
        location_mult = self._get_location_multiplier(location)
        
        # Apply experience multiplier
        exp_mult = 1 + (experience_years * 0.05)  # 5% per year
        exp_mult = min(exp_mult, 2.0)  # Cap at 2x
        
        # Calculate final range
        salary_min = int(base_min * location_mult * exp_mult)
        salary_max = int(base_max * location_mult * exp_mult)
        salary_median = int(base_median * location_mult * exp_mult)
        
        # Generate insights
        percentile_25 = int(salary_min + (salary_median - salary_min) * 0.5)
        percentile_75 = int(salary_median + (salary_max - salary_median) * 0.5)
        
        # Get market insights from database
        demand = role['demand_level'] if isinstance(role, dict) else role[5]
        growth = role['growth_trend'] if isinstance(role, dict) else role[6]
        competition = role['competition_level'] if isinstance(role, dict) else role[7]
        skills_json = role['top_skills'] if isinstance(role, dict) else role[8]
        
        try:
            top_skills = json.loads(skills_json) if skills_json else []
        except:
            top_skills = []
        
        return {
            'job_title': job_title,
            'location': location,
            'experience_years': experience_years,
            'salary_range': {
                'min': salary_min,
                'max': salary_max,
                'median': salary_median,
                'percentile_25': percentile_25,
                'percentile_75': percentile_75,
                'currency': 'USD'
            },
            'market_insights': {
                'demand': demand,
                'growth_trend': growth,
                'competition': competition,
                'skills_premium': top_skills
            },
            'comparison': {
                'vs_national_avg': self._compare_to_national(salary_median, base_median),
                'vs_location_avg': self._compare_to_location(salary_median, location)
            }
        }
    
    def _compare_to_national(self, salary, base_median):
        """Compare to national average"""
        diff_pct = ((salary - base_median) / base_median) * 100
        if diff_pct > 10:
            return f'+{int(diff_pct)}% above national avg'
        elif diff_pct < -10:
            return f'{int(diff_pct)}% below national avg'
        return 'On par with national avg'
    
    def _compare_to_location(self, salary, location):
        """Compare to location average"""
        mult = self._get_location_multiplier(location)
        if mult > 1.2:
            return 'Premium market location'
        elif mult < 0.5:
            return 'Lower cost market'
        return 'Average cost market'

# Global instance
salary_insights = SalaryInsightsSystem()

def init_salary_insights_endpoints(app):
    """Initialize salary insights endpoints"""
    from flask import request, jsonify
    
    @app.route('/api/salary/insights', methods=['POST'])
    def get_salary_insights():
        """Get salary insights for a job"""
        data = request.json
        job_title = data.get('jobTitle', 'Software Engineer')
        location = data.get('location', 'Remote')
        experience_years = data.get('experienceYears', 2)
        
        insights = salary_insights.get_salary_insights(
            job_title, location, experience_years
        )
        
        return jsonify(insights)
    
    @app.route('/api/salary/compare', methods=['POST'])
    def compare_salaries():
        """Compare salaries for multiple roles"""
        data = request.json
        roles = data.get('roles', [])
        
        results = []
        for role in roles[:5]:  # Limit to 5 comparisons
            insights = salary_insights.get_salary_insights(
                role.get('title', 'Software Engineer'),
                role.get('location', 'Remote'),
                role.get('experience', 2)
            )
            results.append(insights)
        
        return jsonify({'comparisons': results})
    
    print("✅ Salary insights endpoints initialized")
