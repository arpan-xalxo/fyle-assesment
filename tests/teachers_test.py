from unittest.mock import patch, MagicMock
from core.models.teachers import Teacher 
from core.models.assignments import Assignment,AssignmentStateEnum
from core.apis.assignments.schema import TeacherSchema
import json

def test_get_assignments_teacher_1(client, h_teacher_1, mocker):
    
    mock_assignments = [
        {"id": 1, "teacher_id": 1, "content": "Assignment 1", "state": "SUBMITTED"},
        {"id": 2, "teacher_id": 1, "content": "Assignment 2", "state": "GRADED"},
    ]

    
    mocker.patch(
        "core.models.assignments.Assignment.get_assignments_by_teacher",
        return_value=mock_assignments
    )

    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2, mocker):
    
    mock_assignments = [
        {"id": 3, "teacher_id": 2, "content": "Assignment 3", "state": "SUBMITTED"},
        {"id": 4, "teacher_id": 2, "content": "Assignment 4", "state": "GRADED"},
    ]
    mocker.patch(
        "core.models.assignments.Assignment.get_assignments_by_teacher",
        return_value=mock_assignments
    )

    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2, mocker):
    
    mock_assignment = MagicMock(
        id=1,
        teacher_id=1,  
        student_id=1,
        state="SUBMITTED",
        grade=None
    )
    
    
    mocker.patch(
        "core.models.assignments.Assignment.get_by_id",
        return_value=mock_assignment
    )

    
    mocker.patch("core.db.session.commit")
    mocker.patch("core.db.session.add")

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'FyleError'

def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_list_teachers(client):
    """Test GET /teachers endpoint"""

    headers = {
        'X-Principal': json.dumps({
            'user_id': 1,
            'principal_id': 5  
        })
    }

    response = client.get("principal/teachers",headers=headers)

    assert response.status_code == 200