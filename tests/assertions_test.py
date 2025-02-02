import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

def test_assert_auth_raises_error_when_condition_is_false():
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False, "Custom Unauthorized")
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Custom Unauthorized"

def test_assert_auth_does_not_raise_error_when_condition_is_true():
    try:
        assert_auth(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly")

def test_assert_true_raises_error_when_condition_is_false():
    with pytest.raises(FyleError) as exc_info:
        assert_true(False, "Custom Forbidden")
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "Custom Forbidden"

def test_assert_true_does_not_raise_error_when_condition_is_true():
    try:
        assert_true(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly")

def test_assert_valid_raises_error_when_condition_is_false():
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False, "Custom Bad Request")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Custom Bad Request"

def test_assert_valid_does_not_raise_error_when_condition_is_true():
    try:
        assert_valid(True)
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly")

def test_assert_found_raises_error_when_object_is_none():
    with pytest.raises(FyleError) as exc_info:
        assert_found(None, "Custom Not Found")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "Custom Not Found"

def test_assert_found_does_not_raise_error_when_object_is_not_none():
    try:
        assert_found("some_object")
    except FyleError:
        pytest.fail("FyleError was raised unexpectedly")
