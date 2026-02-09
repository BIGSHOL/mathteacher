"""시드 문제의 concept_id를 최신 시드 데이터 기준으로 업데이트합니다.

--clear 없이 concept_id 매핑만 수정하므로 AI 생성 문제는 보존됩니다.

사용법:
    cd backend
    python -m app.scripts.fix_concept_ids              # 실행
    python -m app.scripts.fix_concept_ids --dry-run    # 검증만
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.core.database import SyncSessionLocal, sync_engine, Base
from app.models.question import Question
from app.seeds import get_all_grade_seed_data


def main():
    parser = argparse.ArgumentParser(description="시드 문제 concept_id 업데이트")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 확인만")
    args = parser.parse_args()

    print("시드 데이터 로드 중...")
    data = get_all_grade_seed_data()

    # 시드 문제의 id → concept_id 매핑
    seed_mapping = {q["id"]: q["concept_id"] for q in data["questions"]}
    print(f"  시드 문제: {len(seed_mapping)}개")

    Base.metadata.create_all(bind=sync_engine)
    db = SyncSessionLocal()

    try:
        # DB에서 시드 문제만 조회
        seed_ids = list(seed_mapping.keys())
        db_questions = db.query(Question).filter(Question.id.in_(seed_ids)).all()
        print(f"  DB에서 찾은 시드 문제: {len(db_questions)}개")

        updated = 0
        skipped = 0
        mismatches = []

        for q in db_questions:
            expected = seed_mapping[q.id]
            if q.concept_id != expected:
                mismatches.append({
                    "id": q.id,
                    "content": q.content[:50],
                    "old": q.concept_id,
                    "new": expected,
                })
                if not args.dry_run:
                    q.concept_id = expected
                updated += 1
            else:
                skipped += 1

        if mismatches:
            print(f"\n  concept_id 불일치 {len(mismatches)}건:")
            for m in mismatches:
                print(f"    {m['id']}: {m['old']} → {m['new']}")
                print(f"      내용: {m['content']}...")
        else:
            print("\n  모든 concept_id가 이미 최신 상태입니다.")

        if not args.dry_run and updated > 0:
            db.commit()
            print(f"\n  {updated}건 업데이트 완료!")
        elif args.dry_run:
            print(f"\n  [DRY-RUN] 변경 예정: {updated}건, 스킵: {skipped}건")
        else:
            print(f"\n  변경 없음. 스킵: {skipped}건")

    finally:
        db.close()


if __name__ == "__main__":
    main()
