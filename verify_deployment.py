import requests
import sys

BASE_URL = "https://jobika-pyt.onrender.com"

def test_endpoint(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {url}...")
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

print("🚀 Starting Deployment Verification...")

# 1. Test Health and DB Status
print("Testing Health Check...")
health_status = test_endpoint("/health")
if health_status == 200:
    try:
        resp = requests.get(f"{BASE_URL}/health")
        data = resp.json()
        print(f"Health Data: {data}")
        
        if data.get('database_type') == 'postgres':
            print("✅ Connected to Postgres")
            if not data.get('tables_exist'):
                print("⚠️ Tables missing in Postgres. Attempting migration...")
                # Run migration
                mig_resp = requests.get(f"{BASE_URL}/migrate")
                print(f"Migration Response: {mig_resp.status_code} - {mig_resp.text}")
                
                # Check health again
                resp = requests.get(f"{BASE_URL}/health")
                data = resp.json()
                print(f"New Health Data: {data}")
                if data.get('tables_exist'):
                    print("✅ Migration Successful! Tables created.")
                else:
                    print("❌ Migration Failed or Tables still missing.")
            else:
                print("✅ Tables exist in Postgres")
        else:
            print(f"⚠️ Using {data.get('database_type')} (Not Postgres)")
            
    except Exception as e:
        print(f"Error parsing health check: {e}")

# 2. Test API Jobs
test_endpoint("/api/jobs")

# 3. Test Auth (Register - expected 400 or 200)
print("\nTesting Registration (Expect 400 for missing data)...")
try:
    resp = requests.post(f"{BASE_URL}/api/auth/register", json={})
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Verification Complete")
