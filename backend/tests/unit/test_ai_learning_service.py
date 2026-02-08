
import pytest
from sqlalchemy import select
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.question import Question
from app.models.user import User
from app.services.ai_learning_service import AiLearningService

@pytest.mark.asyncio
async def test_analyze_weaknesses_returns_low_mastery_concepts(db_session):
    """analyze_weaknesses: 숙련도 80점 미만 개념 반환 확인"""
    # Given
    user = User(id="u1", login_id="u1", name="U1", role="student", hashed_password="pw", is_active=True, level=1, total_xp=0)
    db_session.add(user)
    
    c1 = Concept(id="c1", name="Weak Concept", grade="middle_1", category="concept", part="algebra")
    c2 = Concept(id="c2", name="Strong Concept", grade="middle_1", category="concept", part="algebra")
    db_session.add_all([c1, c2])
    
    m1 = ConceptMastery(student_id="u1", concept_id="c1", mastery_percentage=50)
    m2 = ConceptMastery(student_id="u1", concept_id="c2", mastery_percentage=90)
    db_session.add_all([m1, m2])
    await db_session.commit()
    
    # When
    service = AiLearningService(db_session)
    weaknesses = await service.analyze_weaknesses("u1")
    
    # Then
    assert len(weaknesses) == 1
    assert weaknesses[0]["concept_id"] == "c1"
    assert weaknesses[0]["mastery_score"] == 50

@pytest.mark.asyncio
async def test_get_recommended_questions_from_weakness(db_session):
    """get_recommended_questions: 취약 개념 기반 문제 추천 확인"""
    # Given
    user = User(id="u2", login_id="u2", name="U2", role="student", hashed_password="pw", is_active=True, level=1, total_xp=0)
    db_session.add(user)
    
    c3 = Concept(id="c3", name="Weak C3", grade="middle_1", category="concept", part="algebra")
    db_session.add(c3)
    
    m3 = ConceptMastery(student_id="u2", concept_id="c3", mastery_percentage=40)
    db_session.add(m3)
    
    q1 = Question(id="q1", concept_id="c3", category="concept", part="algebra", question_type="multiple_choice", difficulty=1, content="Q1", options=[], correct_answer="A", points=10, is_active=True)
    q2 = Question(id="q2", concept_id="c3", category="concept", part="algebra", question_type="multiple_choice", difficulty=1, content="Q2", options=[], correct_answer="A", points=10, is_active=True)
    db_session.add_all([q1, q2])
    await db_session.commit()
    
    # When
    service = AiLearningService(db_session)
    questions = await service.get_recommended_questions("u2", count=2)
    
    # Then
    assert len(questions) > 0
    # 추천된 문제가 취약 개념(c3)에 속하는지 확인
    for q in questions:
        assert q.concept_id == "c3"

@pytest.mark.asyncio
async def test_get_recommended_questions_fill_random(db_session):
    """get_recommended_questions: 취약점이 없을 경우 랜덤 문제 추천 확인"""
    # Given
    user = User(id="u3", login_id="u3", name="U3", role="student", hashed_password="pw", is_active=True, level=1, total_xp=0)
    db_session.add(user)
    
    c4 = Concept(id="c4", name="C4", grade="middle_1", category="concept", part="algebra")
    db_session.add(c4)
    
    # 취약점 없음 (숙련도 기록 없음)
    
    q3 = Question(id="q3", concept_id="c4", category="concept", part="algebra", question_type="multiple_choice", difficulty=1, content="Q3", options=[], correct_answer="A", points=10, is_active=True)
    db_session.add(q3)
    await db_session.commit()
    
    # When
    service = AiLearningService(db_session)
    questions = await service.get_recommended_questions("u3", count=1)
    
    # Then
    assert len(questions) == 1
    assert questions[0].id == "q3"
