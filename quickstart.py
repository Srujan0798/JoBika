#!/usr/bin/env python3
"""
Quick start script for JoBika on port 8080 (avoiding macOS AirPlay conflict)
"""
import os
import sys

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Set port
os.environ['PORT'] = '8080'

# Import and run
import server

if __name__ == '____main__':
    print("🚀 Starting JoBika on http://localhost:8080")
    print("📖 API Docs: http://localhost:8080/api/docs/")
    print("📊 Analytics: http://localhost:8080/app/analytics.html")
    print("\n✅ Press Ctrl+C to stop\n")
    server.app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
