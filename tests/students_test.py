from unittest.mock import patch, MagicMock
from core.models.assignments import Assignment,AssignmentStateEnum


def test_get_assignments_student_1(client, h_student_1, mocker):
    
    mock_assignments = [
        {"id": 1, "student_id": 1, "content": "Assignment 1", "state": "DRAFT"},
        {"id": 2, "student_id": 1, "content": "Assignment 2", "state": "SUBMITTED"},
    ]
    mocker.patch(
        "core.models.assignments.Assignment.get_assignments_by_student",
        return_value=mock_assignments
    )

    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400



def test_post_assignment_student_1(client, h_student_1, mocker):
    
    mock_assignment =Assignment(
        id=1,
        student_id=1,
        content="ABCD TESTPOST",
        state=AssignmentStateEnum.DRAFT,
        teacher_id=None
    )
    mocker.patch(
        "core.models.assignments.Assignment.upsert",
        return_value=mock_assignment
    )

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'ABCD TESTPOST'
        }
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == 'ABCD TESTPOST'
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_submit_assignment_student_1(client, h_student_1,create_draft_assignment):
    """First submission should succeed."""
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1,create_draft_assignment):
    """Resubmission should fail because it's no longer in DRAFT state."""
   
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

   
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
