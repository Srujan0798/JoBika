#!/usr/bin/env python3
"""
Comprehensive deployment verification and auto-fix script for JoBika
"""
import requests
import time
import sys

BASE_URL = "https://jobika-pyt.onrender.com"

def check_health():
    """Check if the service is healthy and using postgres"""
    print("🔍 Checking health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service is healthy!")
            print(f"   Database Type: {data.get('database_type', 'unknown')}")
            print(f"   Tables Exist: {data.get('tables_exist', 'unknown')}")
            return data
        else:
            print(f"   ❌ Service returned error: {response.status_code}")
            try:
                print(f"   Error: {response.text[:200]}")
            except:
                pass
            return None
    except requests.exceptions.Timeout:
        print("   ⏱️  Request timed out - service may be starting up")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def run_migration():
    """Run database migration"""
    print("\n🔄 Running database migration...")
    try:
        response = requests.get(f"{BASE_URL}/migrate", timeout=60)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Migration completed!")
            print(f"   Status: {data.get('status', 'unknown')}")
            if 'message' in data:
                print(f"   Message: {data['message']}")
            return True
        else:
            print(f"   ❌ Migration failed: {response.status_code}")
            try:
                print(f"   Error: {response.text[:200]}")
            except:
                pass
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_debug_db():
    """Check debug database endpoint for detailed error info"""
    print("\n🐛 Checking debug database endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/debug-db", timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Database URL Set: {data.get('database_url_set', False)}")
            print(f"   Connection Successful: {data.get('connection_successful', False)}")
            if 'error' in data:
                print(f"   ❌ Error: {data['error']}")
            if 'traceback' in data:
                print(f"   Traceback: {data['traceback'][:300]}...")
            return data
        else:
            print(f"   ❌ Debug endpoint returned error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("JoBika Deployment Verification")
    print("=" * 60)
    
    # Step 1: Check health
    health_data = check_health()
    
    if not health_data:
        print("\n⚠️  Service is not responding properly.")
        print("   Checking debug endpoint for more info...")
        check_debug_db()
        print("\n📋 Next Steps:")
        print("   1. Check Render logs for errors")
        print("   2. Verify PYTHON_VERSION is set to '3.10.12' (not '3.11.53.10.12')")
        print("   3. Verify DATABASE_URL uses the pooler:")
        print("      postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres")
        sys.exit(1)
    
    # Step 2: Check database type
    if health_data.get('database_type') != 'postgres':
        print(f"\n⚠️  Wrong database type: {health_data.get('database_type')}")
        print("   Expected: postgres")
        check_debug_db()
        print("\n📋 Fix: Update DATABASE_URL in Render to use the pooler connection string")
        sys.exit(1)
    
    # Step 3: Check if tables exist
    if not health_data.get('tables_exist'):
        print("\n📊 Database is connected but tables don't exist.")
        print("   Running migration...")
        if run_migration():
            print("\n✅ Migration successful! Verifying...")
            time.sleep(2)
            health_data = check_health()
            if health_data and health_data.get('tables_exist'):
                print("   ✅ Tables now exist!")
            else:
                print("   ⚠️  Tables still don't exist. Check migration logs.")
                sys.exit(1)
        else:
            print("\n❌ Migration failed. Check the logs.")
            sys.exit(1)
    else:
        print("\n✅ Database tables already exist!")
    
    # Step 4: Final verification
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT VERIFICATION COMPLETE")
    print("=" * 60)
    print(f"🌐 Application URL: {BASE_URL}")
    print(f"🏥 Health Check: {BASE_URL}/health")
    print(f"📝 Registration: {BASE_URL}/auth.html")
    print("\n🎉 Your application is ready to use!")

if __name__ == "__main__":
    main()
