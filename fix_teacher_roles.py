"""
Fix Teacher Roles in MongoDB
Updates existing teacher records to include proper role field
"""
from pymongo import MongoClient
import hashlib

# MongoDB Configuration
MONGO_URI = "mongodb+srv://kartikbansal9152_db_user:TDYGu9eIsZpL6k4b@proj101.gfemks2.mongodb.net/?appName=Proj101"
DB_NAME = "ai_proctor_db"

print("="*70)
print("🔧 Fixing Teacher Roles in MongoDB")
print("="*70)

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    print("✅ Connected to MongoDB\n")
    
    # Get all teachers
    teachers = list(db.teachers.find({}))
    print(f"Found {len(teachers)} teacher(s) in database:\n")
    
    for teacher in teachers:
        print(f"  - Username: {teacher.get('username')}")
        print(f"    Role: {teacher.get('role', 'NOT SET')}")
        print(f"    Has password: {'Yes' if teacher.get('password') else 'No'}")
        print()
    
    # Define correct teachers with roles
    correct_teachers = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "teacher1", "password": "teacher123", "role": "teacher"},
        {"username": "proctor", "password": "proctor123", "role": "proctor"}
    ]
    
    print("\n🔄 Updating/Creating teachers with correct roles...\n")
    
    for teacher_data in correct_teachers:
        username = teacher_data['username']
        password = teacher_data['password']
        role = teacher_data['role']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Update or insert teacher
        result = db.teachers.update_one(
            {"username": username},
            {"$set": {
                "username": username,
                "password": hashed_password,
                "role": role
            }},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"  ✅ Created: {username} ({role})")
        elif result.modified_count > 0:
            print(f"  ✅ Updated: {username} ({role})")
        else:
            print(f"  ℹ️  No changes needed: {username} ({role})")
    
    print("\n" + "="*70)
    print("📊 Verification")
    print("="*70 + "\n")
    
    # Verify all teachers
    for teacher_data in correct_teachers:
        username = teacher_data['username']
        teacher = db.teachers.find_one({"username": username})
        
        if teacher:
            role = teacher.get('role', 'NOT SET')
            has_correct_role = role == teacher_data['role']
            
            # Verify password hash
            expected_hash = hashlib.sha256(teacher_data['password'].encode()).hexdigest()
            actual_hash = teacher.get('password', '')
            has_correct_password = expected_hash == actual_hash
            
            status = "✅" if (has_correct_role and has_correct_password) else "❌"
            print(f"{status} {username}:")
            print(f"   Role: {role} {'✓' if has_correct_role else '✗'}")
            print(f"   Password: {'✓' if has_correct_password else '✗'}")
            print()
        else:
            print(f"❌ {username}: NOT FOUND\n")
    
    print("="*70)
    print("✅ Teacher roles fixed successfully!")
    print("="*70)
    
    client.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
