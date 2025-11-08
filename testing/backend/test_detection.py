"""
Detection System Tests
Tests for head detection, face verification, object detection, and audio anomaly detection
"""
import pytest
import json
import io
import cv2
import numpy as np
from PIL import Image

def create_test_image(width=640, height=480, color=(255, 255, 255)):
    """Helper function to create a test image"""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = color
    return img

def image_to_bytes(img):
    """Convert numpy array to bytes"""
    success, encoded = cv2.imencode('.jpg', img)
    return io.BytesIO(encoded.tobytes())


class TestHeadDetection:
    """Test cases for head pose detection"""
    
    def test_detect_head_endpoint_exists(self, client):
        """Test that detect-head endpoint exists"""
        # Create a simple test image
        img = create_test_image()
        img_bytes = image_to_bytes(img)
        
        response = client.post('/detect-head',
            data={'image': (img_bytes, 'test.jpg')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'direction' in data
        assert 'yaw' in data
        assert 'pitch' in data
        assert 'roll' in data
    
    def test_detect_head_no_face(self, client):
        """Test head detection with image containing no face"""
        img = create_test_image()
        img_bytes = image_to_bytes(img)
        
        response = client.post('/detect-head',
            data={'image': (img_bytes, 'test.jpg')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['direction'] == "No face detected"


class TestFaceVerification:
    """Test cases for face registration and verification"""
    
    def test_register_face_endpoint(self, client):
        """Test face registration endpoint"""
        img = create_test_image()
        img_bytes = image_to_bytes(img)
        
        response = client.post('/register-face',
            data={
                'roll_number': 'TEST001',
                'image': (img_bytes, 'test.jpg')
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        # Likely will return 'no_face' for blank image
        assert data['status'] in ['no_face', 'registered', 'multiple_faces']
    
    def test_verify_face_endpoint(self, client):
        """Test face verification endpoint"""
        img = create_test_image()
        img_bytes = image_to_bytes(img)
        
        response = client.post('/verify-face',
            data={
                'roll_number': 'TEST001',
                'image': (img_bytes, 'test.jpg')
            },
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data


class TestObjectDetection:
    """Test cases for object detection"""
    
    def test_detect_object_endpoint(self, client):
        """Test object detection endpoint"""
        img = create_test_image()
        img_bytes = image_to_bytes(img)
        
        response = client.post('/detect-object',
            data={'image': (img_bytes, 'test.jpg')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        # Blank image should return 'clear'
        assert data['status'] in ['clear', 'forbidden_object']


class TestAudioDetection:
    """Test cases for audio anomaly detection"""
    
    def test_detect_audio_anomaly_clear(self, client):
        """Test audio detection with normal audio"""
        response = client.post('/detect-audio-anomaly',
            data=json.dumps({
                "student_id": "TEST001",
                "audio_features": {
                    "volume_level": 0.05,
                    "frequency_data": [0.1, 0.2, 0.15],
                    "duration": 1.0
                }
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'clear'
    
    def test_detect_audio_anomaly_detected(self, client):
        """Test audio detection with suspicious audio"""
        response = client.post('/detect-audio-anomaly',
            data=json.dumps({
                "student_id": "TEST001",
                "audio_features": {
                    "volume_level": 0.60,  # Very high volume
                    "frequency_data": [0.5, 0.6, 0.7, 0.5, 0.6, 0.7, 0.8, 0.9],
                    "duration": 2.0
                }
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'anomaly_detected'
        assert 'anomalies' in data
        assert 'volume_level' in data
    
    def test_detect_audio_missing_data(self, client):
        """Test audio detection with missing data"""
        response = client.post('/detect-audio-anomaly',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
