"""DB 시드 스크립트 - concepts 테이블에 교육과정 개념 데이터를 삽입합니다.

사용법:
    cd backend
    python -m app.data.seed_db

옵션:
    --clear  기존 데이터를 삭제하고 다시 삽입
    --dry-run  실제 삽입 없이 검증만 수행
"""

import argparse
import sys
from pathlib import Path

# backend 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine, Base
from app.models.concept import Concept, concept_prerequisites
from app.data.seed_concepts import ALL_CONCEPTS, get_concept_by_id


def seed_concepts(db: Session, *, clear: bool = False, dry_run: bool = False) -> dict:
    """개념 시드 데이터를 DB에 삽입합니다.

    Returns:
        {"created": int, "skipped": int, "prerequisites": int, "errors": list}
    """
    result = {"created": 0, "skipped": 0, "prerequisites": 0, "errors": []}

    if clear and not dry_run:
        # 선수관계 먼저 삭제
        db.execute(concept_prerequisites.delete())
        db.query(Concept).delete()
        db.commit()
        print("[CLEAR] 기존 concepts 데이터 삭제 완료")

    # 1단계: 개념 삽입
    existing_ids = {c.id for c in db.query(Concept.id).all()}

    for data in ALL_CONCEPTS:
        concept_id = data["id"]

        if concept_id in existing_ids:
            result["skipped"] += 1
            continue

        if dry_run:
            print(f"  [DRY-RUN] {concept_id}: {data['name']} ({data['grade']})")
            result["created"] += 1
            continue

        concept = Concept(
            id=concept_id,
            name=data["name"],
            grade=data["grade"],
            category=data["category"],
            part=data["part"],
            description=data["description"],
            parent_id=data.get("parent_id"),
        )
        db.add(concept)
        result["created"] += 1

    if not dry_run:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            result["errors"].append(f"개념 삽입 실패: {e}")
            return result

    # 2단계: 선수관계 삽입
    all_ids = existing_ids | {d["id"] for d in ALL_CONCEPTS}

    for data in ALL_CONCEPTS:
        concept_id = data["id"]
        prereqs = data.get("prerequisites", [])

        for prereq_id in prereqs:
            if prereq_id not in all_ids:
                result["errors"].append(
                    f"선수관계 오류: {concept_id} → {prereq_id} (존재하지 않는 ID)"
                )
                continue

            if dry_run:
                print(f"  [DRY-RUN] 선수관계: {concept_id} ← {prereq_id}")
                result["prerequisites"] += 1
                continue

            # 중복 체크
            exists = db.execute(
                concept_prerequisites.select().where(
                    concept_prerequisites.c.concept_id == concept_id,
                    concept_prerequisites.c.prerequisite_id == prereq_id,
                )
            ).first()

            if not exists:
                db.execute(
                    concept_prerequisites.insert().values(
                        concept_id=concept_id,
                        prerequisite_id=prereq_id,
                    )
                )
                result["prerequisites"] += 1

    if not dry_run:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            result["errors"].append(f"선수관계 삽입 실패: {e}")

    return result


def print_summary(result: dict) -> None:
    """결과 요약을 출력합니다."""
    print("\n" + "=" * 50)
    print("개념 시드 데이터 삽입 결과")
    print("=" * 50)
    print(f"  생성: {result['created']}개")
    print(f"  스킵 (이미 존재): {result['skipped']}개")
    print(f"  선수관계: {result['prerequisites']}개")

    if result["errors"]:
        print(f"\n  오류 {len(result['errors'])}건:")
        for err in result["errors"]:
            print(f"    - {err}")
    else:
        print("\n  오류: 없음")

    # 학년별 통계
    from collections import Counter
    grade_counts = Counter(d["grade"] for d in ALL_CONCEPTS)
    print("\n  학년별 개념 수:")
    for grade in sorted(grade_counts.keys()):
        print(f"    {grade}: {grade_counts[grade]}개")


def validate_data() -> list[str]:
    """시드 데이터의 무결성을 검증합니다."""
    errors = []
    all_ids = {d["id"] for d in ALL_CONCEPTS}

    # ID 중복 체크
    seen_ids: set[str] = set()
    for d in ALL_CONCEPTS:
        if d["id"] in seen_ids:
            errors.append(f"중복 ID: {d['id']}")
        seen_ids.add(d["id"])

    # 선수관계 존재 여부 체크
    for d in ALL_CONCEPTS:
        for prereq_id in d.get("prerequisites", []):
            if prereq_id not in all_ids:
                errors.append(f"존재하지 않는 선수 ID: {d['id']} → {prereq_id}")

    # parent_id 존재 여부 체크
    for d in ALL_CONCEPTS:
        parent_id = d.get("parent_id")
        if parent_id and parent_id not in all_ids:
            errors.append(f"존재하지 않는 parent_id: {d['id']} → {parent_id}")

    # 순환 참조 체크
    def has_cycle(concept_id: str, visited: set[str]) -> bool:
        if concept_id in visited:
            return True
        visited.add(concept_id)
        concept = get_concept_by_id(concept_id)
        if not concept:
            return False
        for prereq_id in concept.get("prerequisites", []):
            if has_cycle(prereq_id, visited.copy()):
                return True
        return False

    for d in ALL_CONCEPTS:
        if has_cycle(d["id"], set()):
            errors.append(f"순환 참조 감지: {d['id']}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="교육과정 개념 시드 데이터 삽입")
    parser.add_argument("--clear", action="store_true", help="기존 데이터 삭제 후 재삽입")
    parser.add_argument("--dry-run", action="store_true", help="실제 삽입 없이 검증만")
    args = parser.parse_args()

    # 데이터 검증
    print("데이터 무결성 검증 중...")
    validation_errors = validate_data()
    if validation_errors:
        print(f"\n검증 오류 {len(validation_errors)}건:")
        for err in validation_errors:
            print(f"  - {err}")
        if not args.dry_run:
            print("\n오류가 있어 삽입을 중단합니다. --dry-run으로 확인하세요.")
            sys.exit(1)
    else:
        print("검증 통과!")

    print(f"\n총 {len(ALL_CONCEPTS)}개 개념 삽입 시작...")
    if args.dry_run:
        print("[DRY-RUN 모드]")

    # 테이블 생성 확인
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        result = seed_concepts(db, clear=args.clear, dry_run=args.dry_run)
        print_summary(result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
