import asyncio
import logging
import re
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text as sa_text

from app.core.config import settings
from app.core.database import Base, sync_engine, AsyncSessionLocal, SyncSessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Rate Limiter 설정
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def init_db():
    """Initialize database tables and seed data."""
    # Import all models to register them with Base
    from app.models import (
        User, Class, Concept, Question, Test, TestAttempt, AnswerLog,
        Chapter, ChapterProgress, ConceptMastery, DailyTestRecord,
        WrongAnswerReview, Assignment,
    )
    from app.models.user import RefreshToken
    from app.services.auth_service import AuthService

    # 테이블 생성 (없는 테이블만 생성, 기존 데이터 보존)
    Base.metadata.create_all(bind=sync_engine)

    # Seed initial data if database is empty (using sync session)
    db = SyncSessionLocal()
    try:
        if not db.query(User).first():
            auth_service = AuthService(db)

            # Create master (최고 관리자)
            master = User(
                id="master-001",
                login_id="master01",
                name="마스터 관리자",
                role="master",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(master)
            db.flush()

            # Create admin (관리자)
            admin = User(
                id="admin-001",
                login_id="admin01",
                name="테스트 관리자",
                role="admin",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(admin)
            db.flush()

            # Create teacher
            teacher = User(
                id="teacher-001",
                login_id="teacher01",
                name="테스트 강사",
                role="teacher",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(teacher)
            db.flush()

            # Create classes (학년별 테스트반)
            test_class_m1 = Class(
                id="class-001",
                name="중1 테스트반",
                teacher_id="teacher-001",
            )
            test_class_e3 = Class(
                id="class-002",
                name="초3 테스트반",
                teacher_id="teacher-001",
            )
            test_class_h1 = Class(
                id="class-003",
                name="고1 테스트반",
                teacher_id="teacher-001",
            )
            db.add_all([test_class_m1, test_class_e3, test_class_h1])
            db.flush()

            # Create students (학년별 테스트 학생)
            student_m1 = User(
                id="student-001",
                login_id="student01",
                name="테스트 학생(중1)",
                role="student",
                grade="middle_1",
                class_id="class-001",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=3,
                total_xp=450,
                current_streak=5,
                max_streak=7,
            )
            student_e3 = User(
                id="student-002",
                login_id="student02",
                name="테스트 학생(초3)",
                role="student",
                grade="elementary_3",
                class_id="class-002",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            student_h1 = User(
                id="student-003",
                login_id="student03",
                name="테스트 학생(고1)",
                role="student",
                grade="high_1",
                class_id="class-003",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            db.add_all([student_m1, student_e3, student_h1])

            # =============================================
            # 전체 학년 Chapter 데이터 (2022 개정 교육과정)
            # docs/guides/ 가이드 문서 기준 단원 구성
            # 초3~초6: 12단원 (1학기 6 + 2학기 6)
            # 중1: 12단원 (1학기 6 + 2학기 6)
            # 중2: 8단원 (1학기 4 + 2학기 4)
            # 중3: 7단원 (1학기 4 + 2학기 3)
            # 고1(high_1): 7단원 (공통수학1 4 + 공통수학2 3)
            # =============================================
            _chapter_defs = {
                # --- 초등학교 3학년 (12단원) ---
                # 형식: (name, description, concept_ids, semester)
                "e3": ("elementary_3", [
                    ("1. 덧셈과 뺄셈", "세 자리 수의 덧셈과 뺄셈, 받아올림과 받아내림", ["e3-1-1-01", "e3-1-1-02", "e3-1-1-03", "e3-1-1-04", "e3-1-1-05", "e3-1-1-06"], 1),
                    ("2. 평면도형", "선분, 반직선, 직선, 각, 직각", ["e3-1-2-01", "e3-1-2-02", "e3-1-2-03", "e3-1-2-04", "e3-1-2-05", "e3-1-2-06"], 1),
                    ("3. 나눗셈", "등분제, 포함제, 곱셈과 나눗셈의 관계", ["e3-1-3-01", "e3-1-3-02", "e3-1-3-03", "e3-1-3-04"], 1),
                    ("4. 곱셈", "(몇십몇)×(몇), 올림이 있는 곱셈, 분배법칙의 기초", ["e3-1-4-01", "e3-1-4-02", "e3-1-4-03", "e3-1-4-04", "e3-1-4-05"], 1),
                    ("5. 길이와 시간", "km와 m, 시간의 덧셈과 뺄셈", ["e3-1-5-01", "e3-1-5-02", "e3-1-5-03", "e3-1-5-04", "e3-1-5-05", "e3-1-5-06"], 1),
                    ("6. 분수와 소수", "분수의 개념, 소수의 개념, 분수와 소수의 관계", ["e3-1-6-01", "e3-1-6-02", "e3-1-6-03", "e3-1-6-04", "e3-1-6-05", "e3-1-6-06", "e3-1-6-07", "e3-1-6-08"], 1),
                    ("7. 곱셈 (2)", "(몇)×(몇십몇), (몇십몇)×(몇십몇)", ["e3-2-1-01", "e3-2-1-02", "e3-2-1-03", "e3-2-1-04", "e3-2-1-05", "e3-2-1-06", "e3-2-1-07"], 2),
                    ("8. 나눗셈 (2)", "(두 자리 수)÷(한 자리 수), 나머지가 있는 나눗셈", ["e3-2-2-01", "e3-2-2-02", "e3-2-2-03", "e3-2-2-04", "e3-2-2-05", "e3-2-2-06", "e3-2-2-07", "e3-2-2-08"], 2),
                    ("9. 원", "원의 중심, 반지름, 지름, 컴퍼스 사용", ["e3-2-3-01", "e3-2-3-02", "e3-2-3-03", "e3-2-3-04"], 2),
                    ("10. 분수 (2)", "단위분수, 진분수, 가분수, 대분수, 분수의 크기 비교", ["e3-2-4-01", "e3-2-4-02", "e3-2-4-03", "e3-2-4-04", "e3-2-4-05", "e3-2-4-06"], 2),
                    ("11. 들이와 무게", "L와 mL, kg과 g, 들이와 무게의 덧셈과 뺄셈", ["e3-2-5-01", "e3-2-5-02", "e3-2-5-03", "e3-2-5-04", "e3-2-5-05", "e3-2-5-06", "e3-2-5-07", "e3-2-5-08"], 2),
                    ("12. 자료의 정리", "그림그래프, 자료의 분류와 정리", ["e3-2-6-01", "e3-2-6-02", "e3-2-6-03", "e3-2-6-04"], 2),
                ]),
                # --- 초등학교 4학년 (12단원) ---
                "e4": ("elementary_4", [
                    ("1. 큰 수", "만, 억, 조, 수의 크기 비교, 자릿값", ["e4-1-1-01", "e4-1-1-02", "e4-1-1-03", "e4-1-1-04", "e4-1-1-05", "e4-1-1-06"], 1),
                    ("2. 각도", "각의 크기, 예각·직각·둔각, 삼각형 내각의 합", ["e4-1-2-01", "e4-1-2-02", "e4-1-2-03", "e4-1-2-04", "e4-1-2-05", "e4-1-2-06", "e4-1-2-07", "e4-1-2-08"], 1),
                    ("3. 곱셈과 나눗셈", "(세 자리 수)×(두 자리 수), (세 자리 수)÷(두 자리 수)", ["e4-1-3-01", "e4-1-3-02", "e4-1-3-03", "e4-1-3-04", "e4-1-3-05", "e4-1-3-06", "e4-1-3-07"], 1),
                    ("4. 평면도형의 이동", "밀기, 뒤집기, 돌리기", ["e4-1-4-01", "e4-1-4-02", "e4-1-4-03", "e4-1-4-04", "e4-1-4-05"], 1),
                    ("5. 막대그래프", "막대그래프 읽기와 그리기, 눈금 설정", ["e4-1-5-01", "e4-1-5-02", "e4-1-5-03", "e4-1-5-04"], 1),
                    ("6. 규칙 찾기", "수의 배열에서 규칙 찾기, 규칙을 식으로 나타내기", ["e4-1-6-01", "e4-1-6-02", "e4-1-6-03", "e4-1-6-04", "e4-1-6-05"], 1),
                    ("7. 분수의 덧셈과 뺄셈", "진분수·대분수의 덧셈과 뺄셈, 통분", ["e4-2-1-01", "e4-2-1-02", "e4-2-1-03", "e4-2-1-04", "e4-2-1-05", "e4-2-1-06"], 2),
                    ("8. 삼각형", "이등변삼각형, 정삼각형, 예각·직각·둔각삼각형", ["e4-2-2-01", "e4-2-2-02", "e4-2-2-03", "e4-2-2-04", "e4-2-2-05"], 2),
                    ("9. 소수의 덧셈과 뺄셈", "소수 두 자리 수의 덧셈과 뺄셈", ["e4-2-3-01", "e4-2-3-02", "e4-2-3-03", "e4-2-3-04", "e4-2-3-05", "e4-2-3-06", "e4-2-3-07", "e4-2-3-08"], 2),
                    ("10. 사각형", "수직과 평행, 평행사변형, 마름모, 사다리꼴", ["e4-2-4-01", "e4-2-4-02", "e4-2-4-03", "e4-2-4-04", "e4-2-4-05", "e4-2-4-06", "e4-2-4-07"], 2),
                    ("11. 꺾은선그래프", "꺾은선그래프 읽기와 그리기, 변화 추이", ["e4-2-5-01", "e4-2-5-02", "e4-2-5-03", "e4-2-5-04", "e4-2-5-05"], 2),
                    ("12. 다각형", "정다각형, 대각선, 다각형의 내각의 합", ["e4-2-6-01", "e4-2-6-02", "e4-2-6-03", "e4-2-6-04", "e4-2-6-05"], 2),
                ]),
                # --- 초등학교 5학년 (12단원) ---
                "e5": ("elementary_5", [
                    ("1. 자연수의 혼합 계산", "연산의 우선순위, 괄호가 있는 식, 문장제 모델링", ["e5-1-1-01", "e5-1-1-02", "e5-1-1-03", "e5-1-1-04", "e5-1-1-05"], 1),
                    ("2. 약수와 배수", "약수, 배수, 최대공약수, 최소공배수", ["e5-1-2-01", "e5-1-2-02", "e5-1-2-03", "e5-1-2-04", "e5-1-2-05", "e5-1-2-06"], 1),
                    ("3. 규칙과 대응", "두 양 사이의 관계, 대응 관계를 식으로 표현", ["e5-1-3-01", "e5-1-3-02", "e5-1-3-03"], 1),
                    ("4. 약분과 통분", "분수의 기본 성질, 약분, 통분, 크기 비교", ["e5-1-4-01", "e5-1-4-02", "e5-1-4-03", "e5-1-4-04", "e5-1-4-05", "e5-1-4-06"], 1),
                    ("5. 분수의 덧셈과 뺄셈", "이분모 분수의 덧셈과 뺄셈, 대분수 혼합 계산", ["e5-1-5-01", "e5-1-5-02", "e5-1-5-03", "e5-1-5-04", "e5-1-5-05", "e5-1-5-06"], 1),
                    ("6. 다각형의 둘레와 넓이", "직사각형, 평행사변형, 삼각형, 사다리꼴, 마름모의 넓이", ["e5-1-6-01", "e5-1-6-02", "e5-1-6-03", "e5-1-6-04", "e5-1-6-05", "e5-1-6-06", "e5-1-6-07", "e5-1-6-08", "e5-1-6-09"], 1),
                    ("7. 수의 범위와 어림하기", "이상, 이하, 초과, 미만, 올림, 버림, 반올림", ["e5-2-1-01", "e5-2-1-02", "e5-2-1-03", "e5-2-1-04", "e5-2-1-05", "e5-2-1-06", "e5-2-1-07"], 2),
                    ("8. 분수의 곱셈", "(분수)×(자연수), (자연수)×(분수), (분수)×(분수)", ["e5-2-2-01", "e5-2-2-02", "e5-2-2-03", "e5-2-2-04", "e5-2-2-05"], 2),
                    ("9. 합동과 대칭", "합동인 도형, 선대칭, 점대칭", ["e5-2-3-01", "e5-2-3-02", "e5-2-3-03", "e5-2-3-04"], 2),
                    ("10. 소수의 곱셈", "(소수)×(자연수), (소수)×(소수), 곱의 소수점 위치", ["e5-2-4-01", "e5-2-4-02", "e5-2-4-03", "e5-2-4-04", "e5-2-4-05", "e5-2-4-06", "e5-2-4-07"], 2),
                    ("11. 직육면체", "직육면체와 정육면체, 전개도, 겨냥도", ["e5-2-5-01", "e5-2-5-02", "e5-2-5-03", "e5-2-5-04", "e5-2-5-05", "e5-2-5-06"], 2),
                    ("12. 평균과 가능성", "평균 구하기, 가능성의 표현, 경우의 수", ["e5-2-6-01", "e5-2-6-02", "e5-2-6-03", "e5-2-6-04", "e5-2-6-05", "e5-2-6-06"], 2),
                ]),
                # --- 초등학교 6학년 (12단원) ---
                "e6": ("elementary_6", [
                    ("1. 분수의 나눗셈", "(자연수)÷(자연수)의 몫을 분수로, (분수)÷(자연수)", ["e6-1-1-01", "e6-1-1-02", "e6-1-1-03", "e6-1-1-04"], 1),
                    ("2. 각기둥과 각뿔", "각기둥과 각뿔의 구성 요소, 전개도", ["e6-1-2-01", "e6-1-2-02", "e6-1-2-03", "e6-1-2-04", "e6-1-2-05", "e6-1-2-06"], 1),
                    ("3. 소수의 나눗셈", "(소수)÷(자연수), 몫의 소수점 위치", ["e6-1-3-01", "e6-1-3-02", "e6-1-3-03", "e6-1-3-04", "e6-1-3-05", "e6-1-3-06", "e6-1-3-07"], 1),
                    ("4. 비와 비율", "비, 비율, 백분율, 기준량과 비교하는 양", ["e6-1-4-01", "e6-1-4-02", "e6-1-4-03", "e6-1-4-04", "e6-1-4-05", "e6-1-4-06"], 1),
                    ("5. 여러 가지 그래프", "띠그래프, 원그래프, 그래프 해석", ["e6-1-5-01", "e6-1-5-02", "e6-1-5-03", "e6-1-5-04", "e6-1-5-05", "e6-1-5-06", "e6-1-5-07"], 1),
                    ("6. 직육면체의 부피와 겉넓이", "부피 단위, 직육면체의 부피와 겉넓이 구하기", ["e6-1-6-01", "e6-1-6-02", "e6-1-6-03", "e6-1-6-04"], 1),
                    ("7. 분수의 나눗셈 (2)", "(분수)÷(분수), 역수 활용", ["e6-2-1-01", "e6-2-1-02", "e6-2-1-03", "e6-2-1-04", "e6-2-1-05", "e6-2-1-06"], 2),
                    ("8. 소수의 나눗셈 (2)", "(소수)÷(소수), 소수점 이동 원리", ["e6-2-2-01", "e6-2-2-02", "e6-2-2-03", "e6-2-2-04", "e6-2-2-05", "e6-2-2-06"], 2),
                    ("9. 공간과 입체", "쌓기나무, 공간 감각, 위·앞·옆에서 본 모양", ["e6-2-3-01", "e6-2-3-02", "e6-2-3-03", "e6-2-3-04", "e6-2-3-05", "e6-2-3-06"], 2),
                    ("10. 비례식과 비례배분", "비례식의 성질, 비례배분", ["e6-2-4-01", "e6-2-4-02", "e6-2-4-03", "e6-2-4-04", "e6-2-4-05", "e6-2-4-06"], 2),
                    ("11. 원의 넓이", "원주율, 원의 둘레, 원의 넓이", ["e6-2-5-01", "e6-2-5-02", "e6-2-5-03", "e6-2-5-04", "e6-2-5-05", "e6-2-5-06"], 2),
                    ("12. 원기둥, 원뿔, 구", "원기둥의 전개도와 겉넓이, 원뿔, 구의 특징", ["e6-2-6-01", "e6-2-6-02", "e6-2-6-03", "e6-2-6-04"], 2),
                ]),
                # --- 중학교 1학년 (12단원: 1학기 6 + 2학기 6) ---
                "m1": ("middle_1", [
                    # 1학기
                    ("1. 소인수분해", "소수, 합성수, 소인수분해, 최대공약수, 최소공배수", ["m1-1-1-1", "m1-1-1-2", "m1-1-1-3"], 1),
                    ("2. 정수와 유리수", "양수·음수·0, 절댓값, 정수·유리수 사칙연산", ["m1-1-2-1", "m1-1-2-2", "m1-1-2-3"], 1),
                    ("3. 문자의 사용과 식의 계산", "문자 사용, 대수적 관습, 동류항, 식의 값", ["m1-1-3-1", "m1-1-3-2", "m1-1-3-3"], 1),
                    ("4. 일차방정식", "등식의 성질, 이항, 일차방정식의 풀이, 활용", ["m1-1-4-1", "m1-1-4-2", "m1-1-4-3"], 1),
                    ("5. 좌표평면과 그래프", "순서쌍, 좌표, 사분면, 그래프 해석", ["m1-2-1-1", "m1-2-1-2"], 1),
                    ("6. 정비례와 반비례", "정비례 y=ax, 반비례 y=a/x, 그래프", ["m1-2-2-1", "m1-2-2-2", "m1-2-2-3"], 1),
                    # 2학기
                    ("7. 기본 도형과 작도", "점·선·면, 위치 관계, 평행선 성질, 작도, 삼각형 합동", ["m1-2-3-1", "m1-2-3-2", "m1-2-3-3"], 2),
                    ("8. 평면도형의 성질", "다각형 내각·외각의 합, 원과 부채꼴", ["m1-2-4-1", "m1-2-4-2"], 2),
                    ("9. 입체도형의 성질", "다면체, 회전체, 겉넓이와 부피", ["m1-2-5-1", "m1-2-5-2", "m1-2-5-3"], 2),
                    ("10. 자료의 정리와 해석", "줄기와 잎 그림, 도수분포표, 히스토그램, 상대도수", ["m1-2-6-1", "m1-2-6-2", "m1-2-6-3"], 2),
                    ("11. 대푯값", "평균, 중앙값, 최빈값, 상황별 대푯값 선택", ["m1-2-7-1", "m1-2-7-2"], 2),
                    ("12. 산점도와 상관관계", "산점도, 양의 상관관계, 음의 상관관계, 인과관계 구분", ["m1-2-8-1", "m1-2-8-2"], 2),
                ]),
                # --- 중학교 2학년 (8단원: 1학기 4 + 2학기 4) ---
                "m2": ("middle_2", [
                    # 1학기
                    ("1. 유리수와 순환소수", "유한소수 판별, 순환소수, 순환소수의 분수 표현", ["m2-1-1-1", "m2-1-1-2"], 1),
                    ("2. 식의 계산", "지수법칙, 다항식 계산, 동류항, 분배법칙", ["m2-1-2-1", "m2-1-2-2"], 1),
                    ("3. 부등식과 연립방정식", "일차부등식 풀이, 연립일차방정식(가감법·대입법)", ["m2-1-3-1", "m2-1-3-2"], 1),
                    ("4. 일차함수", "기울기, 절편, 그래프, 일차함수와 일차방정식", ["m2-1-4-1", "m2-1-4-2", "m2-1-5-1", "m2-1-5-2"], 1),
                    # 2학기
                    ("5. 도형의 성질", "이등변삼각형, 외심·내심, 평행사변형, 특수사각형", ["m2-2-1-1", "m2-2-1-2", "m2-2-2-1", "m2-2-2-2"], 2),
                    ("6. 도형의 닮음", "닮음 조건(SSS, SAS, AA), 닮음비, 넓이비, 부피비", ["m2-2-3-1", "m2-2-3-2"], 2),
                    ("7. 평행선과 피타고라스 정리", "평행선과 선분의 비, 삼각형 무게중심, 피타고라스 정리", ["m2-2-4-1", "m2-2-4-2"], 2),
                    ("8. 확률", "경우의 수, 합·곱의 법칙, 확률의 기본, 여사건", ["m2-2-5-1", "m2-2-5-2"], 2),
                ]),
                # --- 중학교 3학년 (7단원) ---
                "m3": ("middle_3", [
                    ("1. 실수와 그 연산", "제곱근, 무리수, 실수의 대소, 근호 계산, 분모의 유리화", ["m3-1-1-1", "m3-1-1-2", "m3-1-1-3"], 1),
                    ("2. 다항식의 곱셈과 인수분해", "곱셈공식, 인수분해, 완전제곱식", ["m3-1-2-1", "m3-1-2-2", "m3-1-2-3"], 1),
                    ("3. 이차방정식", "인수분해·완전제곱식·근의 공식 풀이, 판별식", ["m3-1-3-1", "m3-1-3-2", "m3-1-3-3"], 1),
                    ("4. 이차함수", "y=ax², 표준형, 일반형, 꼭짓점, 최대·최소", ["m3-1-4-1", "m3-1-4-2", "m3-1-4-3"], 1),
                    ("5. 삼각비", "sin·cos·tan 정의, 특수각, 삼각형 넓이", ["m3-2-1-1", "m3-2-1-2"], 2),
                    ("6. 원의 성질", "원주각, 중심각, 접선, 내접 사각형", ["m3-2-2-1", "m3-2-2-2", "m3-2-2-3"], 2),
                    ("7. 통계", "대푯값, 산점도, 상관관계, 상자그림", ["m3-2-3-1", "m3-2-3-2", "m3-2-3-3"], 2),
                ]),
                # --- 고1 (7단원: 공통수학1 4단원 + 공통수학2 3단원) ---
                "h1": ("high_1", [
                    # 공통수학1 (1학기)
                    ("1. 다항식", "다항식 연산, 항등식, 나머지정리, 인수분해", ["h1-1-1-1", "h1-1-1-2"], 1),
                    ("2. 방정식과 부등식", "복소수, 이차방정식, 이차함수, 이차부등식", ["h1-1-2-1", "h1-1-2-2"], 1),
                    ("3. 경우의 수", "합·곱의 법칙, 순열, 조합", ["h1-1-3-1", "h1-1-3-2"], 1),
                    ("4. 행렬", "행렬의 덧셈·뺄셈·실수배·곱셈 (2×2 한정)", ["h1-1-4-1", "h1-1-4-2"], 1),
                    # 공통수학2 (2학기)
                    ("5. 도형의 방정식", "평면좌표, 직선·원의 방정식, 평행이동·대칭이동", ["h1-2-1-1", "h1-2-1-2", "h1-2-1-3", "h1-2-1-4"], 2),
                    ("6. 집합과 명제", "집합 연산, 명제와 조건, 절대부등식", ["h1-2-2-1", "h1-2-2-2", "h1-2-2-3"], 2),
                    ("7. 함수", "합성함수, 역함수, 유리함수, 무리함수", ["h1-2-3-1", "h1-2-3-2", "h1-2-3-3"], 2),
                ]),
            }

            all_new_chapters = {}
            for prefix, (grade, ch_list) in _chapter_defs.items():
                grade_chapters = []
                semester_counters: dict[int, int] = {}
                for idx, (name, desc, cids, semester) in enumerate(ch_list, 1):
                    semester_counters[semester] = semester_counters.get(semester, 0) + 1
                    ch_num = semester_counters[semester]
                    # 단원명에서 기존 번호를 제거하고 학기별 번호로 교체
                    clean_name = re.sub(r'^\d+\.\s*', '', name)
                    display_name = f"{ch_num}. {clean_name}"
                    ch = Chapter(
                        id=f"chapter-{prefix}-{idx:02d}",
                        name=display_name,
                        grade=grade,
                        semester=semester,
                        chapter_number=ch_num,
                        description=desc,
                        concept_ids=cids,
                        mastery_threshold=90,
                        final_test_pass_score=90,
                        require_teacher_approval=False,
                        is_active=True,
                    )
                    db.add(ch)
                    grade_chapters.append(ch)
                all_new_chapters[prefix] = grade_chapters

            db.flush()

            # 각 학년 단원 선수관계 설정 (순차)
            # lazy='raise' 때문에 직접 테이블에 insert
            from app.models.chapter import chapter_prerequisites
            for grade_chapters in all_new_chapters.values():
                for i in range(1, len(grade_chapters)):
                    db.execute(chapter_prerequisites.insert().values(
                        chapter_id=grade_chapters[i].id,
                        prerequisite_id=grade_chapters[i - 1].id
                    ))

            # 각 테스트 학생에게 1단원 해제 (학습 시작 가능)
            _unlock_defs = [
                ("student-001", "chapter-m1-01", "m1-1-1-1"),      # 중1
                ("student-002", "chapter-e3-01", None),            # 초3
                ("student-003", "chapter-h1-01", None),            # 고1
            ]
            for sid, ch_id, concept_id in _unlock_defs:
                db.add(ChapterProgress(
                    student_id=sid,
                    chapter_id=ch_id,
                    is_unlocked=True,
                    unlocked_at=datetime.now(timezone.utc),
                ))
                if concept_id:
                    db.add(ConceptMastery(
                        student_id=sid,
                        concept_id=concept_id,
                        is_unlocked=True,
                        unlocked_at=datetime.now(timezone.utc),
                    ))

            db.commit()
            print("Database seeded with initial data")
        else:
            # 기존 테스트 유저의 grade 동기화 (코드와 DB 불일치 해결)
            TEST_USER_GRADES = {
                "student-001": "middle_1",
                "student-002": "elementary_3",
                "student-003": "high_1",
            }
            updated = 0
            for user_id, expected_grade in TEST_USER_GRADES.items():
                user = db.query(User).filter(User.id == user_id).first()
                if user and user.grade != expected_grade:
                    user.grade = expected_grade
                    updated += 1
            if updated:
                db.commit()
                logger.info(f"Updated {updated} test user grades")
    finally:
        db.close()


def load_seed_data():
    """Load structured seed data (concepts, questions, tests) from seeds module."""
    from app.models.concept import Concept
    from app.models.question import Question
    from app.models.test import Test

    db = SyncSessionLocal()
    try:
        # Check if seed data already loaded (by checking for seed-style concept IDs)
        seed_exists = db.query(Concept).filter(Concept.id.like("e3-%")).first()
        if seed_exists:
            logger.info("Seed data already loaded, skipping")
            return

        logger.info("Loading seed data from seeds module...")
        from app.seeds import get_all_grade_seed_data
        data = get_all_grade_seed_data()

        existing_concepts = {c.id for c in db.query(Concept.id).all()}
        existing_questions = {q.id for q in db.query(Question.id).all()}
        existing_tests = {t.id for t in db.query(Test.id).all()}

        # Concepts
        created_concepts = 0
        for c in data["concepts"]:
            if c["id"] not in existing_concepts:
                db.add(Concept(
                    id=c["id"], name=c["name"], grade=c["grade"],
                    category=c["category"], part=c["part"],
                    description=c.get("description", ""),
                    parent_id=c.get("parent_id"),
                ))
                created_concepts += 1
        db.flush()

        # Questions
        created_questions = 0
        for q in data["questions"]:
            if q["id"] not in existing_questions:
                db.add(Question(
                    id=q["id"], concept_id=q["concept_id"],
                    category=q["category"], part=q["part"],
                    question_type=q["question_type"], difficulty=q["difficulty"],
                    content=q["content"], options=q.get("options"),
                    correct_answer=q["correct_answer"],
                    explanation=q.get("explanation", ""),
                    points=q.get("points", 10),
                    blank_config=q.get("blank_config"),
                ))
                created_questions += 1
        db.flush()

        # Tests
        created_tests = 0
        for t in data["tests"]:
            if t["id"] not in existing_tests:
                db.add(Test(
                    id=t["id"], title=t["title"],
                    description=t.get("description", ""),
                    grade=t["grade"], concept_ids=t["concept_ids"],
                    question_ids=t["question_ids"],
                    question_count=t.get("question_count", len(t["question_ids"])),
                    time_limit_minutes=t.get("time_limit_minutes"),
                    is_adaptive=t.get("is_adaptive", False),
                    is_active=t.get("is_active", True),
                    use_question_pool=t.get("use_question_pool", False),
                    questions_per_attempt=t.get("questions_per_attempt"),
                    shuffle_options=t.get("shuffle_options", True),
                ))
                created_tests += 1

        db.commit()
        logger.info(
            f"Seed data loaded: {created_concepts} concepts, "
            f"{created_questions} questions, {created_tests} tests"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to load seed data: {e}")
    finally:
        db.close()


def update_chapter_concept_ids():
    """서버 시작 시 챕터 concept_ids를 최신 매핑으로 갱신."""
    from app.models.chapter import Chapter

    # 전체 학년 단원-개념 매핑 (시드 데이터 concept ID 기준)
    CHAPTER_CONCEPT_MAP = {
        # --- 초3 ---
        "chapter-e3-01": ["e3-1-1-01", "e3-1-1-02", "e3-1-1-03", "e3-1-1-04", "e3-1-1-05", "e3-1-1-06"],
        "chapter-e3-02": ["e3-1-2-01", "e3-1-2-02", "e3-1-2-03", "e3-1-2-04", "e3-1-2-05", "e3-1-2-06"],
        "chapter-e3-03": ["e3-1-3-01", "e3-1-3-02", "e3-1-3-03", "e3-1-3-04"],
        "chapter-e3-04": ["e3-1-4-01", "e3-1-4-02", "e3-1-4-03", "e3-1-4-04", "e3-1-4-05"],
        "chapter-e3-05": ["e3-1-5-01", "e3-1-5-02", "e3-1-5-03", "e3-1-5-04", "e3-1-5-05", "e3-1-5-06"],
        "chapter-e3-06": ["e3-1-6-01", "e3-1-6-02", "e3-1-6-03", "e3-1-6-04", "e3-1-6-05", "e3-1-6-06", "e3-1-6-07", "e3-1-6-08"],
        "chapter-e3-07": ["e3-2-1-01", "e3-2-1-02", "e3-2-1-03", "e3-2-1-04", "e3-2-1-05", "e3-2-1-06", "e3-2-1-07"],
        "chapter-e3-08": ["e3-2-2-01", "e3-2-2-02", "e3-2-2-03", "e3-2-2-04", "e3-2-2-05", "e3-2-2-06", "e3-2-2-07", "e3-2-2-08"],
        "chapter-e3-09": ["e3-2-3-01", "e3-2-3-02", "e3-2-3-03", "e3-2-3-04"],
        "chapter-e3-10": ["e3-2-4-01", "e3-2-4-02", "e3-2-4-03", "e3-2-4-04", "e3-2-4-05", "e3-2-4-06"],
        "chapter-e3-11": ["e3-2-5-01", "e3-2-5-02", "e3-2-5-03", "e3-2-5-04", "e3-2-5-05", "e3-2-5-06", "e3-2-5-07", "e3-2-5-08"],
        "chapter-e3-12": ["e3-2-6-01", "e3-2-6-02", "e3-2-6-03", "e3-2-6-04"],
        # --- 초4 ---
        "chapter-e4-01": ["e4-1-1-01", "e4-1-1-02", "e4-1-1-03", "e4-1-1-04", "e4-1-1-05", "e4-1-1-06"],
        "chapter-e4-02": ["e4-1-2-01", "e4-1-2-02", "e4-1-2-03", "e4-1-2-04", "e4-1-2-05", "e4-1-2-06", "e4-1-2-07", "e4-1-2-08"],
        "chapter-e4-03": ["e4-1-3-01", "e4-1-3-02", "e4-1-3-03", "e4-1-3-04", "e4-1-3-05", "e4-1-3-06", "e4-1-3-07"],
        "chapter-e4-04": ["e4-1-4-01", "e4-1-4-02", "e4-1-4-03", "e4-1-4-04", "e4-1-4-05"],
        "chapter-e4-05": ["e4-1-5-01", "e4-1-5-02", "e4-1-5-03", "e4-1-5-04"],
        "chapter-e4-06": ["e4-1-6-01", "e4-1-6-02", "e4-1-6-03", "e4-1-6-04", "e4-1-6-05"],
        "chapter-e4-07": ["e4-2-1-01", "e4-2-1-02", "e4-2-1-03", "e4-2-1-04", "e4-2-1-05", "e4-2-1-06"],
        "chapter-e4-08": ["e4-2-2-01", "e4-2-2-02", "e4-2-2-03", "e4-2-2-04", "e4-2-2-05"],
        "chapter-e4-09": ["e4-2-3-01", "e4-2-3-02", "e4-2-3-03", "e4-2-3-04", "e4-2-3-05", "e4-2-3-06", "e4-2-3-07", "e4-2-3-08"],
        "chapter-e4-10": ["e4-2-4-01", "e4-2-4-02", "e4-2-4-03", "e4-2-4-04", "e4-2-4-05", "e4-2-4-06", "e4-2-4-07"],
        "chapter-e4-11": ["e4-2-5-01", "e4-2-5-02", "e4-2-5-03", "e4-2-5-04", "e4-2-5-05"],
        "chapter-e4-12": ["e4-2-6-01", "e4-2-6-02", "e4-2-6-03", "e4-2-6-04", "e4-2-6-05"],
        # --- 초5 ---
        "chapter-e5-01": ["e5-1-1-01", "e5-1-1-02", "e5-1-1-03", "e5-1-1-04", "e5-1-1-05"],
        "chapter-e5-02": ["e5-1-2-01", "e5-1-2-02", "e5-1-2-03", "e5-1-2-04", "e5-1-2-05", "e5-1-2-06"],
        "chapter-e5-03": ["e5-1-3-01", "e5-1-3-02", "e5-1-3-03"],
        "chapter-e5-04": ["e5-1-4-01", "e5-1-4-02", "e5-1-4-03", "e5-1-4-04", "e5-1-4-05", "e5-1-4-06"],
        "chapter-e5-05": ["e5-1-5-01", "e5-1-5-02", "e5-1-5-03", "e5-1-5-04", "e5-1-5-05", "e5-1-5-06"],
        "chapter-e5-06": ["e5-1-6-01", "e5-1-6-02", "e5-1-6-03", "e5-1-6-04", "e5-1-6-05", "e5-1-6-06", "e5-1-6-07", "e5-1-6-08", "e5-1-6-09"],
        "chapter-e5-07": ["e5-2-1-01", "e5-2-1-02", "e5-2-1-03", "e5-2-1-04", "e5-2-1-05", "e5-2-1-06", "e5-2-1-07"],
        "chapter-e5-08": ["e5-2-2-01", "e5-2-2-02", "e5-2-2-03", "e5-2-2-04", "e5-2-2-05"],
        "chapter-e5-09": ["e5-2-3-01", "e5-2-3-02", "e5-2-3-03", "e5-2-3-04"],
        "chapter-e5-10": ["e5-2-4-01", "e5-2-4-02", "e5-2-4-03", "e5-2-4-04", "e5-2-4-05", "e5-2-4-06", "e5-2-4-07"],
        "chapter-e5-11": ["e5-2-5-01", "e5-2-5-02", "e5-2-5-03", "e5-2-5-04", "e5-2-5-05", "e5-2-5-06"],
        "chapter-e5-12": ["e5-2-6-01", "e5-2-6-02", "e5-2-6-03", "e5-2-6-04", "e5-2-6-05", "e5-2-6-06"],
        # --- 초6 ---
        "chapter-e6-01": ["e6-1-1-01", "e6-1-1-02", "e6-1-1-03", "e6-1-1-04"],
        "chapter-e6-02": ["e6-1-2-01", "e6-1-2-02", "e6-1-2-03", "e6-1-2-04", "e6-1-2-05", "e6-1-2-06"],
        "chapter-e6-03": ["e6-1-3-01", "e6-1-3-02", "e6-1-3-03", "e6-1-3-04", "e6-1-3-05", "e6-1-3-06", "e6-1-3-07"],
        "chapter-e6-04": ["e6-1-4-01", "e6-1-4-02", "e6-1-4-03", "e6-1-4-04", "e6-1-4-05", "e6-1-4-06"],
        "chapter-e6-05": ["e6-1-5-01", "e6-1-5-02", "e6-1-5-03", "e6-1-5-04", "e6-1-5-05", "e6-1-5-06", "e6-1-5-07"],
        "chapter-e6-06": ["e6-1-6-01", "e6-1-6-02", "e6-1-6-03", "e6-1-6-04"],
        "chapter-e6-07": ["e6-2-1-01", "e6-2-1-02", "e6-2-1-03", "e6-2-1-04", "e6-2-1-05", "e6-2-1-06"],
        "chapter-e6-08": ["e6-2-2-01", "e6-2-2-02", "e6-2-2-03", "e6-2-2-04", "e6-2-2-05", "e6-2-2-06"],
        "chapter-e6-09": ["e6-2-3-01", "e6-2-3-02", "e6-2-3-03", "e6-2-3-04", "e6-2-3-05", "e6-2-3-06"],
        "chapter-e6-10": ["e6-2-4-01", "e6-2-4-02", "e6-2-4-03", "e6-2-4-04", "e6-2-4-05", "e6-2-4-06"],
        "chapter-e6-11": ["e6-2-5-01", "e6-2-5-02", "e6-2-5-03", "e6-2-5-04", "e6-2-5-05", "e6-2-5-06"],
        "chapter-e6-12": ["e6-2-6-01", "e6-2-6-02", "e6-2-6-03", "e6-2-6-04"],
        # --- 중1 ---
        "chapter-m1-01": ["m1-1-1-1", "m1-1-1-2", "m1-1-1-3"],
        "chapter-m1-02": ["m1-1-2-1", "m1-1-2-2", "m1-1-2-3"],
        "chapter-m1-03": ["m1-1-3-1", "m1-1-3-2", "m1-1-3-3"],
        "chapter-m1-04": ["m1-1-4-1", "m1-1-4-2", "m1-1-4-3"],
        "chapter-m1-05": ["m1-2-1-1", "m1-2-1-2"],
        "chapter-m1-06": ["m1-2-2-1", "m1-2-2-2", "m1-2-2-3"],
        "chapter-m1-07": ["m1-2-3-1", "m1-2-3-2", "m1-2-3-3"],
        "chapter-m1-08": ["m1-2-4-1", "m1-2-4-2"],
        "chapter-m1-09": ["m1-2-5-1", "m1-2-5-2", "m1-2-5-3"],
        "chapter-m1-10": ["m1-2-6-1", "m1-2-6-2", "m1-2-6-3"],
        "chapter-m1-11": ["m1-2-7-1", "m1-2-7-2"],
        "chapter-m1-12": ["m1-2-8-1", "m1-2-8-2"],
        # --- 중2 ---
        "chapter-m2-01": ["m2-1-1-1", "m2-1-1-2"],
        "chapter-m2-02": ["m2-1-2-1", "m2-1-2-2"],
        "chapter-m2-03": ["m2-1-3-1", "m2-1-3-2"],
        "chapter-m2-04": ["m2-1-4-1", "m2-1-4-2", "m2-1-5-1", "m2-1-5-2"],
        "chapter-m2-05": ["m2-2-1-1", "m2-2-1-2", "m2-2-2-1", "m2-2-2-2"],
        "chapter-m2-06": ["m2-2-3-1", "m2-2-3-2"],
        "chapter-m2-07": ["m2-2-4-1", "m2-2-4-2"],
        "chapter-m2-08": ["m2-2-5-1", "m2-2-5-2"],
        # --- 중3 ---
        "chapter-m3-01": ["m3-1-1-1", "m3-1-1-2", "m3-1-1-3"],
        "chapter-m3-02": ["m3-1-2-1", "m3-1-2-2", "m3-1-2-3"],
        "chapter-m3-03": ["m3-1-3-1", "m3-1-3-2", "m3-1-3-3"],
        "chapter-m3-04": ["m3-1-4-1", "m3-1-4-2", "m3-1-4-3"],
        "chapter-m3-05": ["m3-2-1-1", "m3-2-1-2"],
        "chapter-m3-06": ["m3-2-2-1", "m3-2-2-2", "m3-2-2-3"],
        "chapter-m3-07": ["m3-2-3-1", "m3-2-3-2", "m3-2-3-3"],
        # --- 고1 (h1+h2 통합) ---
        "chapter-h1-01": ["h1-1-1-1", "h1-1-1-2"],
        "chapter-h1-02": ["h1-1-2-1", "h1-1-2-2"],
        "chapter-h1-03": ["h1-1-3-1", "h1-1-3-2"],
        "chapter-h1-04": ["h1-1-4-1", "h1-1-4-2"],
        "chapter-h1-05": ["h1-2-1-1", "h1-2-1-2", "h1-2-1-3", "h1-2-1-4"],
        "chapter-h1-06": ["h1-2-2-1", "h1-2-2-2", "h1-2-2-3"],
        "chapter-h1-07": ["h1-2-3-1", "h1-2-3-2", "h1-2-3-3"],
    }

    db = SyncSessionLocal()
    try:
        updated = 0
        missing = 0
        for chapter_id, concept_ids in CHAPTER_CONCEPT_MAP.items():
            ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not ch:
                missing += 1
                logger.warning(f"Chapter not found: {chapter_id}")
                continue
            if ch.concept_ids != concept_ids:
                logger.info(f"Updating {chapter_id}: {ch.concept_ids} -> {concept_ids}")
                ch.concept_ids = concept_ids
                updated += 1

        # 항상 오늘의 0문제 일일 테스트 정리 (매핑 변경 여부와 무관)
        _cleanup_today_daily_tests(db)
        db.commit()

        if updated:
            logger.info(f"Updated concept_ids for {updated} chapters (missing: {missing}), cleaned up today's daily tests")
        else:
            logger.info(f"All {len(CHAPTER_CONCEPT_MAP)} chapter concept_ids already up to date (missing: {missing})")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update chapter concept_ids: {e}", exc_info=True)
    finally:
        db.close()


def _cleanup_today_daily_tests(db):
    """오늘의 0문제/미완료 일일 테스트 정리. 완료된 테스트는 보존."""
    from app.models.daily_test_record import DailyTestRecord
    from app.models.test import Test
    from app.models.test_attempt import TestAttempt
    from app.models.answer_log import AnswerLog

    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).date().isoformat()
    # 0문제이거나 아직 시작 안 한 테스트만 정리 (완료된 것은 보존)
    records = db.query(DailyTestRecord).filter(
        DailyTestRecord.date == today,
        DailyTestRecord.status != "completed",
    ).all()
    if not records:
        return

    for record in records:
        test_id = record.test_id
        attempt_id = record.attempt_id
        # 1. DailyTestRecord 먼저 삭제 (test_id, attempt_id FK 해소)
        db.delete(record)
        db.flush()
        # 2. AnswerLog 삭제 (attempt_id FK 해소)
        if attempt_id:
            db.query(AnswerLog).filter(AnswerLog.attempt_id == attempt_id).delete()
        # 3. TestAttempt 삭제
        if attempt_id:
            db.query(TestAttempt).filter(TestAttempt.id == attempt_id).delete()
        # 4. Test 삭제
        if test_id:
            db.query(Test).filter(Test.id == test_id).delete()

    logger.info(f"Cleaned up {len(records)} daily test records for today ({today})")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup - 동기 DB 초기화를 스레드풀에서 실행 (이벤트 루프 블로킹 방지)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, init_db)
    await loop.run_in_executor(None, load_seed_data)
    await loop.run_in_executor(None, update_chapter_concept_ids)
    yield
    # Shutdown


app = FastAPI(
    title="Math Test API",
    description="수학 개념 및 연산 테스트 프로그램 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Rate Limiter를 앱에 연결
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Math Test API", "docs": "/docs"}


# Exception handler - 프로덕션에서는 상세 에러 정보 숨김
# CORS 헤더를 에러 응답에도 추가하여 브라우저에서 에러 내용을 확인할 수 있도록 함
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 서버 로그에는 상세 정보 기록 (디버깅용)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Origin 헤더 확인하여 CORS 헤더 추가
    origin = request.headers.get("origin", "")
    cors_headers = {}
    if origin in settings.BACKEND_CORS_ORIGINS:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }

    # 클라이언트 응답에는 환경에 따라 다르게 처리
    if settings.ENV == "development":
        # 개발 환경: 디버깅을 위해 상세 에러 표시
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            },
            headers=cors_headers,
        )
    else:
        # 프로덕션/스테이징: 보안을 위해 일반적인 에러 메시지만 표시
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
                }
            },
            headers=cors_headers,
        )


# API v1 Router
from app.api.v1 import api_router

app.include_router(api_router)
