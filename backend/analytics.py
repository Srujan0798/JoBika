import json
from datetime import datetime, timedelta
from collections import Counter
from database import get_db_connection, get_placeholder

def get_application_stats(user_id):
    """Get application statistics for a user"""
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    P = get_placeholder(db_type)
    
    # Total applications
    cursor.execute(f'SELECT COUNT(*) FROM applications WHERE user_id = {P}', (user_id,))
    # Handle different cursor types (RealDictCursor vs standard)
    result = cursor.fetchone()
    if isinstance(result, dict):
        total_applications = result['count']
    else:
        total_applications = result[0]
    
    # Applications by status
    cursor.execute(f'''
        SELECT status, COUNT(*) as count 
        FROM applications 
        WHERE user_id = {P} 
        GROUP BY status
    ''', (user_id,))
    status_breakdown = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Applications over time (last 7 days)
    dates = []
    counts = []
    
    # Date truncation syntax
    date_func = "DATE(applied_date)" if db_type == 'sqlite' else "applied_date::DATE"
    
    for i in range(6, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        cursor.execute(f'''
            SELECT COUNT(*) as count
            FROM applications 
            WHERE user_id = {P} AND {date_func} = {P}
        ''', (user_id, date))
        
        result = cursor.fetchone()
        if isinstance(result, dict):
            count = result['count']
        else:
            count = result[0]
            
        dates.append(date)
        counts.append(count)
        
    conn.close()
    
    return {
        'total': total_applications,
        'breakdown': status_breakdown,
        'timeline': {
            'dates': dates,
            'counts': counts
        }
    }

def get_market_insights():
    """Get general market insights from job listings"""
    conn, _ = get_db_connection()
    cursor = conn.cursor()
    
    # Top skills in demand (simple keyword counting from skills column)
    cursor.execute('SELECT required_skills FROM jobs')
    all_skills = []
    for row in cursor.fetchall():
        try:
            # Handle different column names if schema changed (skills vs required_skills)
            # In init_db we used required_skills
            skills_json = row['required_skills']
            if skills_json:
                skills = json.loads(skills_json)
                all_skills.extend(skills)
        except:
            pass
            
    skill_counts = Counter(all_skills).most_common(5)
    
    conn.close()
    
    return {
        'top_skills': [{'name': s[0], 'count': s[1]} for s in skill_counts]
    }
