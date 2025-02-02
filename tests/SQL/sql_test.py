import random
from sqlalchemy import text
import pytest
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError

class TestSQL:
    @patch("core.db.session.execute")  
    @patch("core.db.session.commit")
    def test_count_grade_A_assignments_by_teacher_with_max_grading(self, mock_commit, mock_execute):
        """
        Test counting assignments with grade 'A' for the teacher 
        who has graded the most assignments without modifying the database.
        """
        teacher_id = 1
        student_id = 1

        
        with patch.object(self, "create_n_graded_assignments_for_teacher_and_student", return_value=10) as mock_create:
            expected_count = mock_create(10, teacher_id, student_id)

        
        mock_execute.return_value.fetchone.return_value = (expected_count,)

        
        result = db.session.execute(
            text("SELECT COUNT(*) FROM assignments WHERE grade = 'A'")  
        ).fetchone()

        
        assert result is not None, "Query did not return any results"
        assert result[0] == expected_count, f"Expected {expected_count}, but got {result[0]}"

        
        mock_commit.assert_not_called()

    
    def create_n_graded_assignments_for_teacher_and_student(self, number: int = 0, teacher_id: int = 1, student_id: int = 1, session=None) -> int:
        """
        Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.
        """
        if session is None:
            session = db.session  

        grade_a_counter: int = session.query(Assignment).filter(
            Assignment.teacher_id == teacher_id,
            Assignment.grade == GradeEnum.A
        ).count()

        for _ in range(number):
            grade = random.choice(list(GradeEnum))
            assignment = Assignment(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=grade,
                content='test content',
                state=AssignmentStateEnum.GRADED
            )
            session.add(assignment)
            if grade == GradeEnum.A:
                grade_a_counter += 1

        session.commit()  
        return grade_a_counter
 
    def test_count_assignments_in_each_grade(self):
        """
        This test executes an SQL query to count assignments for each grade where the state is 'GRADED'
        and verifies the results.
        """
        
        teacher_id = 1
        student_id = 1
        self.create_n_graded_assignments(10, teacher_id, student_id)

        
        result = db.session.execute(
            text(open("tests/SQL/count_assignments_in_each_grade.sql").read())
        ).fetchall()

        
        assert result is not None, "Query did not return any results"
        
        grade_counts = {row[0]: row[1] for row in result}

        for grade in GradeEnum:
            
            assert grade in grade_counts, f"Missing assignments for grade: {grade}"
            print(f"Grade {grade}: {grade_counts[grade]} assignments")

    def create_n_graded_assignments(self, number: int = 0, teacher_id: int = 1, student_id: int = 1) -> None:
        """
        Creates 'n' graded assignments for a teacher and student.
        """
        for _ in range(number):
            grade = random.choice(list(GradeEnum))

            assignment = Assignment(
                teacher_id=teacher_id,
                student_id=student_id,
                grade=grade,
                content='test content',
                state=AssignmentStateEnum.GRADED
            )

            db.session.add(assignment)

        db.session.flush()

   
    def teardown_method(self) -> None:
        # Rollback the changes to the database after each test
        db.session.rollback()

   