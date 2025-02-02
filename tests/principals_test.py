from core.models.assignments import AssignmentStateEnum, GradeEnum,Assignment
from unittest.mock import patch, MagicMock
import json
from core import db
from core.models.principals import Principal



def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal,create_draft_assignment_for_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400



def test_grade_assignment(client, h_teacher_1, mocker):
    
    mock_assignment = Assignment(
        id=1,
        teacher_id=1, 
        student_id=1,
        state=AssignmentStateEnum.SUBMITTED,
        grade=None
    )

    print(f"Mock assignment before grading: {mock_assignment}")

    mocker.patch(
        "core.models.assignments.Assignment.get_by_id",
        return_value=mock_assignment
    )

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 200


def test_regrade_assignment(client, h_principal, mocker):
   
    mock_assignment = Assignment(
        id=4,
        teacher_id=1,  
        student_id=1,
        state=AssignmentStateEnum.SUBMITTED,
        grade=GradeEnum.C.value  
    )

    print(f"Mock assignment before regrading: {mock_assignment}")

    
    mocker.patch(
        "core.models.assignments.Assignment.get_by_id",
        return_value=mock_assignment
    )

    
    mocker.patch("core.db.session.commit")

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value  
        },
        headers=h_principal
    )

    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value

    assert response.json['data']['grade'] == GradeEnum.B.value

def test_list_principals(client):
    """Test fetching all principals without hitting the database"""
    

    mock_principals = [
        Principal(id=1, user_id=101),
        Principal(id=2, user_id=102)
    ]

    with patch.object(Principal, "query") as mock_query:
        mock_query.all.return_value = mock_principals

        response = client.get("/principal/principals", 
        headers={"X-Principal": '{"user_id":1,"principal_id":1}'})

        assert response.status_code == 200
        data = response.json["data"]
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2

def test_list_principals_empty(client):
    """Test fetching principals when there are none in the database"""
    
    with patch.object(Principal, "query") as mock_query:
        mock_query.all.return_value = []  
        response = client.get("/principal/principals", 
        headers={"X-Principal": '{"user_id":1,"principal_id":1}'})

        assert response.status_code == 200

        data = response.json["data"]
        assert data == []  
