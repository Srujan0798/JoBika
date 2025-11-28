"""
Resume Version Comparison for JoBika
Compare different versions of resumes
"""

import difflib
import json
from datetime import datetime
from database import get_db_connection, get_placeholder

class ResumeComparer:
    """Compare resume versions"""
    
    def __init__(self):
        pass
    
    def compare_versions(self, version_id_1, version_id_2):
        """
        Compare two resume versions
        
        Returns:
            dict with differences and statistics
        """
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        try:
            # Get both versions
            cursor.execute(f'SELECT * FROM resume_versions WHERE id = {P}', (version_id_1,))
            version1 = cursor.fetchone()
            
            cursor.execute(f'SELECT * FROM resume_versions WHERE id = {P}', (version_id_2,))
            version2 = cursor.fetchone()
            
            if not version1 or not version2:
                return {'error': 'One or both versions not found'}
            
            # Compare content
            content1 = version1['customized_content'] or version1['original_content'] or ''
            content2 = version2['customized_content'] or version2['original_content'] or ''
            
            # Get differences
            diff = self._get_text_diff(content1, content2)
            
            # Compare metadata
            skills1 = set(json.loads(version1['skills'] or '[]')) # Note: schema uses 'skills' not 'skills_added'
            skills2 = set(json.loads(version2['skills'] or '[]'))
            
            # Assuming keywords are part of content or stored elsewhere, but schema only has content/skills
            # We'll skip keywords for now if not in schema, or assume they are in skills
            
            result = {
                'version1': {
                    'id': version1['id'],
                    'version_name': version1['version_name'], # Schema uses version_name
                    'created_at': version1['created_at'],
                    'match_score': version1['match_score']
                },
                'version2': {
                    'id': version2['id'],
                    'version_name': version2['version_name'],
                    'created_at': version2['created_at'],
                    'match_score': version2['match_score']
                },
                'differences': {
                    'text_diff': diff,
                    'skills_added': list(skills2 - skills1),
                    'skills_removed': list(skills1 - skills2)
                },
                'statistics': {
                    'similarity_percentage': self._calculate_similarity(content1, content2),
                    'length_change': len(content2) - len(content1),
                    'skills_change': len(skills2) - len(skills1)
                }
            }
            
            return result
            
        finally:
            conn.close()
    
    def _get_text_diff(self, text1, text2):
        """Get line-by-line differences"""
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))
        
        # Format diff for display
        formatted_diff = []
        for line in diff[:100]:  # Limit to first 100 lines
            if line.startswith('  '):
                formatted_diff.append({'type': 'unchanged', 'content': line[2:]})
            elif line.startswith('- '):
                formatted_diff.append({'type': 'removed', 'content': line[2:]})
            elif line.startswith('+ '):
                formatted_diff.append({'type': 'added', 'content': line[2:]})
        
        return formatted_diff
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity percentage"""
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return round(matcher.ratio() * 100, 2)
    
    def get_version_history(self, user_id, limit=10):
        """Get resume version history for user"""
        conn, db_type = get_db_connection()
        cursor = conn.cursor()
        P = get_placeholder(db_type)
        
        try:
            cursor.execute(f'''
                SELECT id, version_name, match_score, created_at
                FROM resume_versions
                WHERE user_id = {P}
                ORDER BY created_at DESC
                LIMIT {limit}
            ''', (user_id,))
            
            versions = [dict(row) for row in cursor.fetchall()]
            return versions
            
        finally:
            conn.close()

# Global instance
resume_comparer = ResumeComparer()

def init_resume_comparison_endpoints(app):
    """Initialize resume comparison endpoints"""
    from flask import request, jsonify
    
    @app.route('/api/resume/versions/compare', methods=['POST'])
    def compare_resume_versions():
        """Compare two resume versions"""
        from server import verify_token
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.json
        version_id_1 = data.get('versionId1')
        version_id_2 = data.get('versionId2')
        
        if not version_id_1 or not version_id_2:
            return jsonify({'error': 'Both version IDs required'}), 400
        
        result = resume_comparer.compare_versions(version_id_1, version_id_2)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
    
    @app.route('/api/resume/versions/history')
    def get_version_history():
        """Get resume version history"""
        from server import verify_token
        
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        limit = int(request.args.get('limit', 10))
        versions = resume_comparer.get_version_history(user_id, limit)
        
        return jsonify(versions)
    
    print("✅ Resume comparison endpoints initialized")
