"""
API Endpoint Tests
Tests for core API endpoints
"""
import pytest
import json
import io
from datetime import datetime

class TestAlertsAPI:
    """Test cases for alerts endpoints"""
    
    def test_get_alerts(self, client):
        """Test retrieving alerts"""
        response = client.get('/alerts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_log_alert_success(self, client):
        """Test logging an alert"""
        response = client.post('/log-alert',
            data=json.dumps({
                "student_id": "TEST001",
                "direction": "Looking Left",
                "time": datetime.now().isoformat()
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
    
    def test_log_alert_missing_data(self, client):
        """Test logging alert with missing data"""
        response = client.post('/log-alert',
            data=json.dumps({
                "student_id": "TEST001"
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestConnectionAPI:
    """Test database connection endpoints"""
    
    def test_connection_endpoint(self, client):
        """Test database connection test endpoint"""
        response = client.get('/test-connection')
        assert response.status_code in [200, 500]
        data = json.loads(response.data)
        assert "status" in data
    
    def test_registered_faces(self, client):
        """Test registered faces endpoint"""
        response = client.get('/registered-faces')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "registered_faces" in data
        assert isinstance(data["registered_faces"], list)
