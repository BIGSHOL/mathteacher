"""서비스 유닛 테스트 (RED 상태 - 실패하는 테스트)."""

import pytest


class TestAuthService:
    """인증 서비스 테스트."""

    def test_hash_password(self) -> None:
        """비밀번호 해싱."""
        from app.services.auth_service import AuthService

        service = AuthService()
        password = "test_password_123"
        hashed = service.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self) -> None:
        """올바른 비밀번호 검증."""
        from app.services.auth_service import AuthService

        service = AuthService()
        password = "test_password_123"
        hashed = service.hash_password(password)

        assert service.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self) -> None:
        """잘못된 비밀번호 검증."""
        from app.services.auth_service import AuthService

        service = AuthService()
        password = "test_password_123"
        hashed = service.hash_password(password)

        assert service.verify_password("wrong_password", hashed) is False

    def test_create_access_token(self) -> None:
        """액세스 토큰 생성."""
        from app.services.auth_service import AuthService

        service = AuthService()
        user_id = "test-user-id"
        token = service.create_access_token(user_id)

        assert token is not None
        assert len(token) > 0

    def test_create_refresh_token(self) -> None:
        """리프레시 토큰 생성."""
        from app.services.auth_service import AuthService

        service = AuthService()
        user_id = "test-user-id"
        token = service.create_refresh_token(user_id)

        assert token is not None
        assert len(token) > 0

    def test_verify_access_token(self) -> None:
        """액세스 토큰 검증."""
        from app.services.auth_service import AuthService

        service = AuthService()
        user_id = "test-user-id"
        token = service.create_access_token(user_id)
        payload = service.verify_token(token)

        assert payload is not None
        assert payload["sub"] == user_id


class TestGradingService:
    """채점 서비스 테스트."""

    def test_grade_correct_answer(self) -> None:
        """정답 채점."""
        from app.services.grading_service import GradingService

        service = GradingService()
        result = service.grade_answer(
            question_id="q1",
            selected_answer="A",
            correct_answer="A",
            points=10,
        )

        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_grade_incorrect_answer(self) -> None:
        """오답 채점."""
        from app.services.grading_service import GradingService

        service = GradingService()
        result = service.grade_answer(
            question_id="q1",
            selected_answer="B",
            correct_answer="A",
            points=10,
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 0

    def test_calculate_combo_bonus(self) -> None:
        """콤보 보너스 계산."""
        from app.services.grading_service import GradingService

        service = GradingService()

        # 1콤보: 기본 점수
        assert service.calculate_combo_bonus(1, 10) == 10

        # 3콤보: 1.5배
        assert service.calculate_combo_bonus(3, 10) == 15

        # 5콤보: 2배
        assert service.calculate_combo_bonus(5, 10) == 20


class TestGamificationService:
    """게이미피케이션 서비스 테스트."""

    def test_calculate_xp_earned(self) -> None:
        """XP 계산."""
        from app.services.gamification_service import GamificationService

        service = GamificationService()
        xp = service.calculate_xp(
            score=80,
            max_score=100,
            combo_max=5,
            time_bonus=True,
        )

        assert xp > 0

    def test_check_level_up(self) -> None:
        """레벨업 체크."""
        from app.services.gamification_service import GamificationService

        service = GamificationService()

        # 레벨 1 → 2 (필요 XP: 100)
        result = service.check_level_up(current_level=1, current_xp=50, xp_earned=60)

        assert result["level_up"] is True
        assert result["new_level"] == 2

    def test_no_level_up(self) -> None:
        """레벨업 없음."""
        from app.services.gamification_service import GamificationService

        service = GamificationService()

        result = service.check_level_up(current_level=1, current_xp=50, xp_earned=30)

        assert result["level_up"] is False
        assert result["new_level"] is None

    def test_update_streak(self) -> None:
        """스트릭 업데이트."""
        from app.services.gamification_service import GamificationService

        service = GamificationService()

        # 어제 활동 있음 → 스트릭 증가
        result = service.update_streak(
            current_streak=5,
            last_activity_date="2024-01-14",
            today="2024-01-15",
        )

        assert result["new_streak"] == 6

    def test_streak_broken(self) -> None:
        """스트릭 끊김."""
        from app.services.gamification_service import GamificationService

        service = GamificationService()

        # 이틀 전 활동 → 스트릭 리셋
        result = service.update_streak(
            current_streak=5,
            last_activity_date="2024-01-13",
            today="2024-01-15",
        )

        assert result["new_streak"] == 1


class TestStatsService:
    """통계 서비스 테스트."""

    def test_calculate_accuracy_rate(self) -> None:
        """정답률 계산."""
        from app.services.stats_service import StatsService

        service = StatsService()
        rate = service.calculate_accuracy_rate(correct=8, total=10)

        assert rate == 80.0

    def test_calculate_accuracy_rate_zero_total(self) -> None:
        """총 문제 0개일 때 정답률."""
        from app.services.stats_service import StatsService

        service = StatsService()
        rate = service.calculate_accuracy_rate(correct=0, total=0)

        assert rate == 0.0

    def test_identify_weak_concepts(self) -> None:
        """취약 개념 식별."""
        from app.services.stats_service import StatsService

        service = StatsService()
        answer_logs = [
            {"concept_id": "c1", "is_correct": True},
            {"concept_id": "c1", "is_correct": False},
            {"concept_id": "c2", "is_correct": False},
            {"concept_id": "c2", "is_correct": False},
            {"concept_id": "c3", "is_correct": True},
            {"concept_id": "c3", "is_correct": True},
        ]

        weak = service.identify_weak_concepts(answer_logs, threshold=60.0)

        # c2는 0% 정답률이므로 취약
        assert "c2" in [c["concept_id"] for c in weak]
        # c3는 100% 정답률이므로 취약 아님
        assert "c3" not in [c["concept_id"] for c in weak]
