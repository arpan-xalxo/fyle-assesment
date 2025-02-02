import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    """Test that FyleError is initialized with correct status_code and message."""
    status_code = 404
    message = "Not Found"
    
    error = FyleError(status_code, message)
    
    assert error.status_code == status_code
    assert error.message == message

def test_fyle_error_to_dict():
    """Test that the to_dict method of FyleError returns the expected dictionary."""
    status_code = 400
    message = "Bad Request"
    
    error = FyleError(status_code, message)
    
    expected_dict = {"message": message}
    assert error.to_dict() == expected_dict



def test_fyle_error_with_custom_status_code():
    """Test that custom status_code works correctly."""
    status_code = 422
    message = "Unprocessable Entity"
    
    error = FyleError(status_code, message)
    
    assert error.status_code == status_code
    assert error.message == message
