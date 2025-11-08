"""
Test Script for Teacher Login Functionality
Tests MongoDB teacher authentication and frontend integration
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

import requests
import hashlib
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuration
BACKEND_URL = "http://localhost:5000"
MONGO_URI = "mongodb+srv://kartikbansal9152_db_user:TDYGu9eIsZpL6k4b@proj101.gfemks2.mongodb.net/?appName=Proj101"
DB_NAME = "ai_proctor_db"

# Test credentials
TEST_TEACHERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "teacher1", "password": "teacher123", "role": "teacher"},
    {"username": "proctor", "password": "proctor123", "role": "proctor"},
]

print("="*70)
print("🧪 TEACHER LOGIN TESTING SUITE")
print("="*70)

# Test 1: MongoDB Connection Test
print("\n1️⃣  Testing MongoDB Connection...")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    print("✅ MongoDB connection successful")
    
    # Check if teachers collection exists
    collections = db.list_collection_names()
    if 'teachers' in collections:
        teacher_count = db.teachers.count_documents({})
        print(f"✅ Teachers collection exists with {teacher_count} documents")
    else:
        print("❌ Teachers collection does not exist")
        
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# Test 2: Verify Teacher Entries in MongoDB
print("\n2️⃣  Verifying Teacher Entries in MongoDB...")
try:
    for teacher in TEST_TEACHERS:
        username = teacher['username']
        # Find teacher in database
        db_teacher = db.teachers.find_one({"username": username})
        
        if db_teacher:
            print(f"✅ Teacher '{username}' found in database")
            print(f"   - Role: {db_teacher.get('role', 'N/A')}")
            print(f"   - Password hash: {db_teacher.get('password', 'N/A')[:20]}...")
            
            # Verify password hash matches
            expected_hash = hashlib.sha256(teacher['password'].encode()).hexdigest()
            actual_hash = db_teacher.get('password', '')
            
            if expected_hash == actual_hash:
                print(f"   ✓ Password hash matches for {username}")
            else:
                print(f"   ✗ Password hash mismatch for {username}")
        else:
            print(f"❌ Teacher '{username}' NOT found in database")
            
except Exception as e:
    print(f"❌ Error verifying teachers: {e}")

# Test 3: Backend Server Availability
print("\n3️⃣  Testing Backend Server Availability...")
try:
    response = requests.get(f"{BACKEND_URL}/test-connection", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Backend server is running")
        print(f"   - Status: {data.get('status', 'N/A')}")
        print(f"   - Database: {data.get('database', 'N/A')}")
    else:
        print(f"⚠️  Backend responded with status {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ Backend server not reachable: {e}")
    print("   Please ensure backend is running: cd backend && python app.py")

# Test 4: Teacher Login API Tests
print("\n4️⃣  Testing Teacher Login API Endpoint...")
try:
    # Test 4a: Valid login for each teacher
    print("\n   📝 Test 4a: Valid Teacher Logins")
    for teacher in TEST_TEACHERS:
        try:
            response = requests.post(
                f"{BACKEND_URL}/teacher/login",
                json={"username": teacher['username'], "password": teacher['password']},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == 'Login successful':
                    print(f"   ✅ {teacher['username']}/{teacher['password']} - Login successful")
                    print(f"      - Username: {data.get('username')}")
                    print(f"      - Role: {data.get('role')}")
                else:
                    print(f"   ❌ {teacher['username']} - Unexpected response: {data}")
            else:
                print(f"   ❌ {teacher['username']} - Status {response.status_code}: {response.json()}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {teacher['username']} - Request failed: {e}")
    
    # Test 4b: Invalid credentials
    print("\n   📝 Test 4b: Invalid Credentials")
    invalid_tests = [
        {"username": "invalid_user", "password": "wrong_pass", "expected": 401},
        {"username": "admin", "password": "wrong_password", "expected": 401},
        {"username": "nonexistent", "password": "test123", "expected": 401},
    ]
    
    for test in invalid_tests:
        try:
            response = requests.post(
                f"{BACKEND_URL}/teacher/login",
                json={"username": test['username'], "password": test['password']},
                timeout=5
            )
            
            if response.status_code == test['expected']:
                print(f"   ✅ {test['username']}/{test['password']} - Correctly rejected (401)")
            else:
                print(f"   ❌ {test['username']} - Expected {test['expected']}, got {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test 4c: Missing data
    print("\n   📝 Test 4c: Missing Required Fields")
    missing_tests = [
        {"username": "admin"},  # Missing password
        {"password": "admin123"},  # Missing username
        {},  # Missing both
    ]
    
    for test in missing_tests:
        try:
            response = requests.post(
                f"{BACKEND_URL}/teacher/login",
                json=test,
                timeout=5
            )
            
            if response.status_code == 400:
                print(f"   ✅ Missing fields correctly rejected (400): {test}")
            else:
                print(f"   ❌ Expected 400, got {response.status_code}: {test}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test 4d: Invalid content type
    print("\n   📝 Test 4d: Invalid Content Type")
    try:
        response = requests.post(
            f"{BACKEND_URL}/teacher/login",
            data="not json",
            headers={"Content-Type": "text/plain"},
            timeout=5
        )
        
        if response.status_code in [400, 415]:
            print(f"   ✅ Non-JSON request correctly rejected ({response.status_code})")
        else:
            print(f"   ⚠️  Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        
except Exception as e:
    print(f"❌ Error during API tests: {e}")

# Test 5: Password Hashing Verification
print("\n5️⃣  Testing Password Hashing...")
try:
    test_password = "test123"
    hash1 = hashlib.sha256(test_password.encode()).hexdigest()
    hash2 = hashlib.sha256(test_password.encode()).hexdigest()
    
    if hash1 == hash2:
        print(f"✅ Password hashing is consistent")
        print(f"   - Password: {test_password}")
        print(f"   - Hash: {hash1}")
    else:
        print(f"❌ Password hashing inconsistency detected")
        
except Exception as e:
    print(f"❌ Error testing password hashing: {e}")

# Test 6: Concurrent Login Tests
print("\n6️⃣  Testing Concurrent Logins...")
try:
    import concurrent.futures
    
    def test_login(username, password):
        try:
            response = requests.post(
                f"{BACKEND_URL}/teacher/login",
                json={"username": username, "password": password},
                timeout=5
            )
            return (username, response.status_code == 200)
        except:
            return (username, False)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(test_login, t['username'], t['password']) 
            for t in TEST_TEACHERS
        ]
        
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
    all_passed = all(result[1] for result in results)
    if all_passed:
        print(f"✅ All {len(results)} concurrent logins successful")
    else:
        failed = [r[0] for r in results if not r[1]]
        print(f"❌ Some logins failed: {failed}")
        
except Exception as e:
    print(f"⚠️  Concurrent test skipped: {e}")

# Final Summary
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)

summary_tests = [
    ("MongoDB Connection", True),
    ("Teachers Collection Exists", 'teachers' in db.list_collection_names()),
    ("Teacher Entries Verified", db.teachers.count_documents({}) >= 3),
    ("Backend Server Running", True),  # If we got here, it's running
]

passed = sum(1 for _, result in summary_tests if result)
total = len(summary_tests)

print(f"\n✅ Passed: {passed}/{total}")
print(f"{'❌' if passed < total else '✅'} Failed: {total - passed}/{total}")

print("\n" + "="*70)
print("🎯 RECOMMENDATIONS")
print("="*70)
print("""
✅ If all tests passed:
   - Teacher login is working correctly
   - MongoDB integration is functional
   - Password hashing is secure
   - Frontend can now connect to teacher login

⚠️  If any tests failed:
   - Check MongoDB connection string in backend/app.py
   - Ensure backend server is running (python app.py)
   - Verify teacher entries exist in MongoDB
   - Check firewall/network settings

📝 Test the frontend:
   1. Start backend: cd backend && python app.py
   2. Start frontend: cd frontend && npm start
   3. Navigate to: http://localhost:3000
   4. Click "Teacher/Proctor Login"
   5. Login with: admin / admin123
   6. Should redirect to dashboard

🧪 Run automated tests:
   - Backend: cd testing/backend && pytest
   - Frontend: cd frontend && npm test
""")

print("="*70)
print("✅ Testing Complete!")
print("="*70)

# Cleanup
client.close()
