import pytest
import json
from tests import app
from core import db
from core.models.assignments import Assignment
from core.models.students import Student
from core.models.teachers import Teacher
from unittest.mock import patch

from core.libs import helpers


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for testing and rolls back after the test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(options={"bind": connection})

    original_session = db.session  # Save the original session
    db.session = session
    yield session  

    session.rollback()  
    session.close()
    transaction.rollback()
    connection.close()

    db.session = original_session  # Restoring original session after test


@pytest.fixture
def create_draft_assignment(db_session):
    """Ensure assignment id=2 is always a draft before tests."""
    assignment = Assignment(id=2, student_id=1, state="DRAFT", content="Sample content")
    db_session.merge(assignment) 
    db_session.commit()


@pytest.fixture
def create_draft_assignment_for_principal(db_session):
    """Ensure assignment id=5 is always a draft before tests."""
    assignment = Assignment(id=5, student_id=1, state="DRAFT", content="Sample content")
    db_session.merge(assignment)  
    db_session.commit()


@pytest.fixture
def create_submitted_assignment_for_principal(db_session):
    """Ensure assignment id=4 is always in SUBMITTED state before tests."""
    assignment = Assignment(
        id=4,
        student_id=1,
        teacher_id=1, 
        state="SUBMITTED",
        content="Sample content"
    )
    db_session.merge(assignment)  
    db_session.commit()






    
