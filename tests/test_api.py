"""
API tests
Тесты API
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Cyberbullying" in response.text


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_valid_text():
    """Test text analysis with valid input"""
    response = client.post(
        "/api/analyze",
        json={
            "text": "Hello, how are you?",
            "language": "en"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "is_cyberbullying" in data
    assert "classification" in data
    assert "confidence" in data["classification"]


def test_analyze_bullying_text():
    """Test detection of bullying text"""
    response = client.post(
        "/api/analyze",
        json={
            "text": "You are stupid and I hate you",
            "language": "en"
        }
    )
    assert response.status_code == 200
    assert response.json()["is_cyberbullying"] == True


def test_history():
    """Test history endpoint"""
    response = client.get("/api/history?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
