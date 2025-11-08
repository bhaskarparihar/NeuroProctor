"""
Authentication Tests
Tests for student and teacher login endpoints
"""
import pytest
import json

class TestStudentAuth:
    """Test cases for student authentication"""
    
    def test_student_login_success(self, client, db):
        """Test successful student login"""
        # Create a test student if not exists
        if db is not None:
            try:
                db.students.update_one(
                    {"roll_number": "TEST001"},
                    {"$set": {
                        "username": "test_user",
                        "roll_number": "TEST001",
                        "password": "test123"
                    }},
                    upsert=True
                )
            except Exception as e:
                print(f"Error creating test student: {e}")
        
        response = client.post('/login',
            data=json.dumps({
                "username": "test_user",
                "rollNumber": "TEST001",
                "password": "test123"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Login successful"
    
    def test_student_login_invalid_credentials(self, client):
        """Test student login with invalid credentials"""
        response = client.post('/login',
            data=json.dumps({
                "username": "invalid_user",
                "rollNumber": "INVALID",
                "password": "wrong_password"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Invalid credentials"
    
    def test_student_login_missing_data(self, client):
        """Test student login with missing data"""
        response = client.post('/login',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 400]


class TestTeacherAuth:
    """Test cases for teacher authentication"""
    
    def test_teacher_login_success(self, client, db):
        """Test successful teacher login"""
        import hashlib
        
        # Ensure test teacher exists
        if db is not None:
            try:
                db.teachers.update_one(
                    {"username": "test_teacher"},
                    {"$set": {
                        "username": "test_teacher",
                        "password": hashlib.sha256("test123".encode()).hexdigest(),
                        "role": "teacher"
                    }},
                    upsert=True
                )
            except Exception as e:
                print(f"Error creating test teacher: {e}")
        
        response = client.post('/teacher/login',
            data=json.dumps({
                "username": "test_teacher",
                "password": "test123"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Login successful"
        assert data["username"] == "test_teacher"
    
    def test_teacher_login_invalid_credentials(self, client):
        """Test teacher login with invalid credentials"""
        response = client.post('/teacher/login',
            data=json.dumps({
                "username": "invalid_teacher",
                "password": "wrong_password"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["message"] == "Invalid credentials"
    
    def test_teacher_login_missing_data(self, client):
        """Test teacher login with missing username or password"""
        response = client.post('/teacher/login',
            data=json.dumps({"username": "teacher1"}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        
        response = client.post('/teacher/login',
            data=json.dumps({"password": "password"}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_teacher_login_no_json(self, client):
        """Test teacher login with no JSON data"""
        response = client.post('/teacher/login',
            data="not json",
            content_type='text/plain'
        )
        
        # Flask returns 415 (Unsupported Media Type) for non-JSON content type
        # or 400 (Bad Request) if it accepts but can't parse
        assert response.status_code in [400, 415]
