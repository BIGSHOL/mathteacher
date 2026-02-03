"""통합 시드 스크립트 - 개념/문제/테스트를 DB에 삽입합니다.

시드 파일(app/seeds/)의 구조화된 ID가 그대로 DB에 보존됩니다.
Gemini 생성 데이터도 동일한 파이프라인을 통해 DB에 저장됩니다.

사용법:
    cd backend
    python -m app.scripts.seed_all              # 전체 시드
    python -m app.scripts.seed_all --dry-run    # 검증만
    python -m app.scripts.seed_all --clear      # 기존 삭제 후 재삽입
    python -m app.scripts.seed_all --grade elementary_5  # 특정 학년만
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine, Base
from app.models.concept import Concept
from app.models.question import Question
from app.models.test import Test
from app.seeds import get_all_grade_seed_data


# ─── 유효성 검증 ───


def validate_seed_data(data: dict) -> list[str]:
    """시드 데이터 무결성을 검증합니다."""
    errors = []
    concepts = data["concepts"]
    questions = data["questions"]
    tests = data["tests"]

    concept_ids = set()
    question_ids = set()
    test_ids = set()

    # 1) 개념 ID 중복 검사
    for c in concepts:
        cid = c["id"]
        if cid in concept_ids:
            errors.append(f"[개념] 중복 ID: {cid}")
        concept_ids.add(cid)

    # 2) 문제 ID 중복 + concept_id 참조 검사
    for q in questions:
        qid = q["id"]
        if qid in question_ids:
            errors.append(f"[문제] 중복 ID: {qid}")
        question_ids.add(qid)

        if q["concept_id"] not in concept_ids:
            errors.append(f"[문제] {qid} → 존재하지 않는 concept_id: {q['concept_id']}")

    # 3) 테스트 ID 중복 + 참조 검사
    for t in tests:
        tid = t["id"]
        if tid in test_ids:
            errors.append(f"[테스트] 중복 ID: {tid}")
        test_ids.add(tid)

        for cid in t.get("concept_ids", []):
            if cid not in concept_ids:
                errors.append(f"[테스트] {tid} → 존재하지 않는 concept_id: {cid}")

        for qid in t.get("question_ids", []):
            if qid not in question_ids:
                errors.append(f"[테스트] {tid} → 존재하지 않는 question_id: {qid}")

    return errors


# ─── DB 삽입 ───


def seed_concepts(db: Session, concepts: list[dict], *, clear: bool, dry_run: bool) -> dict:
    """개념 데이터를 DB에 삽입합니다."""
    result = {"created": 0, "skipped": 0, "errors": []}

    if clear and not dry_run:
        deleted = db.query(Concept).delete()
        db.commit()
        print(f"  [CLEAR] concepts {deleted}건 삭제")

    existing = {c.id for c in db.query(Concept.id).all()}

    for data in concepts:
        cid = data["id"]
        if cid in existing:
            result["skipped"] += 1
            continue

        if dry_run:
            result["created"] += 1
            continue

        db.add(Concept(
            id=cid,
            name=data["name"],
            grade=data["grade"],
            category=data["category"],
            part=data["part"],
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
        ))
        result["created"] += 1

    if not dry_run:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            result["errors"].append(str(e))

    return result


def seed_questions(db: Session, questions: list[dict], *, clear: bool, dry_run: bool) -> dict:
    """문제 데이터를 DB에 삽입합니다. 시드 ID가 그대로 보존됩니다."""
    result = {"created": 0, "skipped": 0, "errors": []}

    if clear and not dry_run:
        deleted = db.query(Question).delete()
        db.commit()
        print(f"  [CLEAR] questions {deleted}건 삭제")

    existing = {q.id for q in db.query(Question.id).all()}

    for data in questions:
        qid = data["id"]
        if qid in existing:
            result["skipped"] += 1
            continue

        if dry_run:
            result["created"] += 1
            continue

        db.add(Question(
            id=qid,
            concept_id=data["concept_id"],
            category=data["category"],
            part=data["part"],
            question_type=data["question_type"],
            difficulty=data["difficulty"],
            content=data["content"],
            options=data.get("options"),
            correct_answer=data["correct_answer"],
            explanation=data.get("explanation", ""),
            points=data.get("points", 10),
            blank_config=data.get("blank_config"),
        ))
        result["created"] += 1

    if not dry_run:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            result["errors"].append(str(e))

    return result


def seed_tests(db: Session, tests: list[dict], *, clear: bool, dry_run: bool) -> dict:
    """테스트 데이터를 DB에 삽입합니다. 시드 ID가 그대로 보존됩니다."""
    result = {"created": 0, "skipped": 0, "errors": []}

    if clear and not dry_run:
        deleted = db.query(Test).delete()
        db.commit()
        print(f"  [CLEAR] tests {deleted}건 삭제")

    existing = {t.id for t in db.query(Test.id).all()}

    for data in tests:
        tid = data["id"]
        if tid in existing:
            result["skipped"] += 1
            continue

        if dry_run:
            result["created"] += 1
            continue

        db.add(Test(
            id=tid,
            title=data["title"],
            description=data.get("description", ""),
            grade=data["grade"],
            concept_ids=data["concept_ids"],
            question_ids=data["question_ids"],
            question_count=data.get("question_count", len(data["question_ids"])),
            time_limit_minutes=data.get("time_limit_minutes"),
            is_adaptive=data.get("is_adaptive", False),
            use_question_pool=data.get("use_question_pool", False),
            questions_per_attempt=data.get("questions_per_attempt"),
            shuffle_options=data.get("shuffle_options", True),
        ))
        result["created"] += 1

    if not dry_run:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            result["errors"].append(str(e))

    return result


# ─── 메인 ───


def print_summary(concepts_r: dict, questions_r: dict, tests_r: dict, data: dict):
    """결과 요약을 출력합니다."""
    print("\n" + "=" * 55)
    print("  시드 데이터 삽입 결과")
    print("=" * 55)

    for label, r in [("개념", concepts_r), ("문제", questions_r), ("테스트", tests_r)]:
        status = f"생성 {r['created']} / 스킵 {r['skipped']}"
        if r["errors"]:
            status += f" / 오류 {len(r['errors'])}"
        print(f"  {label:6s}: {status}")

    all_errors = concepts_r["errors"] + questions_r["errors"] + tests_r["errors"]
    if all_errors:
        print(f"\n  오류 목록:")
        for e in all_errors:
            print(f"    - {e}")

    # 학년별 통계
    grade_q = Counter()
    for q in data["questions"]:
        # concept_id에서 학년 추출 (concept-e5-xxx → e5)
        parts = q["concept_id"].split("-")
        if len(parts) >= 2:
            grade_q[parts[1]] += 1

    print(f"\n  학년별 문제 수:")
    for g in sorted(grade_q.keys()):
        print(f"    {g}: {grade_q[g]}문제")

    total = concepts_r["created"] + questions_r["created"] + tests_r["created"]
    print(f"\n  총 {total}건 생성 완료")


def main():
    parser = argparse.ArgumentParser(description="시드 데이터 통합 DB 삽입")
    parser.add_argument("--clear", action="store_true", help="기존 데이터 삭제 후 재삽입")
    parser.add_argument("--dry-run", action="store_true", help="실제 삽입 없이 검증만")
    parser.add_argument("--grade", type=str, help="특정 학년만 시드 (예: elementary_5)")
    args = parser.parse_args()

    # 데이터 로드
    print("시드 데이터 로드 중...")
    try:
        data = get_all_grade_seed_data()
    except Exception as e:
        print(f"ERROR: 시드 데이터 로드 실패: {e}")
        sys.exit(1)

    # 학년 필터링
    if args.grade:
        data["concepts"] = [c for c in data["concepts"] if c.get("grade") == args.grade]
        # 필터링된 concept_id 집합
        cids = {c["id"] for c in data["concepts"]}
        data["questions"] = [q for q in data["questions"] if q.get("concept_id") in cids]
        qids = {q["id"] for q in data["questions"]}
        data["tests"] = [t for t in data["tests"] if t.get("grade") == args.grade]
        print(f"  학년 필터: {args.grade}")

    print(f"  개념: {len(data['concepts'])}개")
    print(f"  문제: {len(data['questions'])}개")
    print(f"  테스트: {len(data['tests'])}개")

    # 유효성 검증
    print("\n데이터 무결성 검증 중...")
    errors = validate_seed_data(data)
    if errors:
        print(f"  검증 오류 {len(errors)}건:")
        for e in errors[:20]:
            print(f"    - {e}")
        if len(errors) > 20:
            print(f"    ... 외 {len(errors) - 20}건")
        if not args.dry_run:
            print("\n오류가 있어 삽입을 중단합니다. --dry-run으로 먼저 확인하세요.")
            sys.exit(1)
    else:
        print("  검증 통과!")

    if args.dry_run:
        print("\n[DRY-RUN] 실제 삽입 없이 종료합니다.")
        return

    # DB 연결
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("\nDB 삽입 시작...")
        opts = {"clear": args.clear, "dry_run": False}

        # 순서: 개념 → 문제 → 테스트 (FK 의존성)
        concepts_r = seed_concepts(db, data["concepts"], **opts)
        questions_r = seed_questions(db, data["questions"], **opts)
        tests_r = seed_tests(db, data["tests"], **opts)

        print_summary(concepts_r, questions_r, tests_r, data)
    finally:
        db.close()


if __name__ == "__main__":
    main()
