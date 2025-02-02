import pytest
from unittest.mock import patch
from flask import jsonify
from core.server import app  
from core.libs.exceptions import FyleError
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError





def test_ready_route(client):
    """Test the readiness endpoint"""
    with patch("core.libs.helpers.get_utc_now", return_value="2025-02-01T12:00:00Z"):
        response = client.get("/")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"
    assert data["time"] == "2025-02-01T12:00:00Z"


def test_handle_fyle_error(client):
    """Test FyleError handling"""
    @app.route("/test-fyle-error")
    def trigger_fyle_error():
        raise FyleError(403, "Forbidden action")

    response = client.get("/test-fyle-error")
    
    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "FyleError"
    assert data["message"] == "Forbidden action"




def test_handle_integrity_error(client):
    """Test IntegrityError handling"""
    @app.route("/test-integrity-error")
    def trigger_integrity_error():
        raise IntegrityError("Duplicate entry", params={}, orig=Exception("UNIQUE constraint failed"))

    response = client.get("/test-integrity-error")
    
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "IntegrityError"
    assert "UNIQUE constraint failed" in data["message"]


def test_handle_http_exception(client):
    """Test HTTPException handling (e.g., 404 Not Found)"""
    response = client.get("/non-existent-route")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "NotFound"
    assert "404 Not Found" in data["message"]


def test_unhandled_exception(client):
    """Test an unhandled exception to ensure it propagates"""
    @app.route("/test-unhandled-exception")
    def trigger_unhandled_exception():
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError, match="Something went wrong"):
        client.get("/test-unhandled-exception")
