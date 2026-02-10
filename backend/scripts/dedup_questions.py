"""중복 문제 탐지 및 제거 스크립트.

동일한 content + concept_id + category + difficulty 조합을 중복으로 판단하고,
각 그룹에서 가장 오래된(먼저 생성된) 문제만 남기고 나머지를 비활성화합니다.

사용법:
    # 분석만 (dry-run, 기본)
    python scripts/dedup_questions.py

    # 실제 비활성화 실행
    python scripts/dedup_questions.py --apply

    # 완전 삭제 (비활성화 대신)
    python scripts/dedup_questions.py --apply --delete
"""

import argparse
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "math_test.db"


def find_duplicates(cursor: sqlite3.Cursor) -> list[dict]:
    """중복 그룹 탐지."""
    cursor.execute("""
        SELECT content, concept_id, category, difficulty, COUNT(*) as cnt
        FROM questions
        WHERE is_active = 1
        GROUP BY content, concept_id, category, difficulty
        HAVING cnt > 1
        ORDER BY cnt DESC
    """)
    groups = []
    for row in cursor.fetchall():
        content, concept_id, category, difficulty, cnt = row
        # 각 그룹의 개별 문제 ID 조회 (생성일 순)
        cursor.execute("""
            SELECT id, created_at
            FROM questions
            WHERE content = ? AND concept_id = ? AND category = ? AND difficulty = ? AND is_active = 1
            ORDER BY created_at ASC
        """, (content, concept_id, category, difficulty))
        ids = cursor.fetchall()
        groups.append({
            "content": content[:80],
            "concept_id": concept_id,
            "category": category,
            "difficulty": difficulty,
            "count": cnt,
            "keep_id": ids[0][0],        # 가장 오래된 것 유지
            "remove_ids": [r[0] for r in ids[1:]],  # 나머지 제거
        })
    return groups


def print_report(groups: list[dict], total_active: int):
    """분석 결과 출력."""
    total_remove = sum(len(g["remove_ids"]) for g in groups)

    print("=" * 70)
    print(f"  중복 문제 분석 결과")
    print("=" * 70)
    print(f"  전체 활성 문제: {total_active}개")
    print(f"  중복 그룹 수:   {len(groups)}개")
    print(f"  제거 대상:      {total_remove}개")
    print(f"  제거 후 문제:   {total_active - total_remove}개")
    print("=" * 70)

    # 상위 20개 그룹 상세
    print(f"\n상위 {min(20, len(groups))}개 중복 그룹:")
    print("-" * 70)
    for i, g in enumerate(groups[:20], 1):
        print(f"  {i:2d}. [{g['count']}x] diff={g['difficulty']} cat={g['category']}")
        print(f"      내용: {g['content']}")
        print(f"      유지: {g['keep_id']}")
        print(f"      제거: {', '.join(g['remove_ids'][:3])}{'...' if len(g['remove_ids']) > 3 else ''}")
        print()


def check_references(cursor: sqlite3.Cursor, question_ids: list[str]) -> dict:
    """제거 대상 문제가 다른 테이블에서 참조되는지 확인."""
    refs = {"answer_logs": 0, "test_questions": 0}

    placeholders = ",".join("?" * len(question_ids))

    # answer_logs 참조
    cursor.execute(f"""
        SELECT COUNT(*) FROM answer_logs WHERE question_id IN ({placeholders})
    """, question_ids)
    refs["answer_logs"] = cursor.fetchone()[0]

    # tests.question_ids (JSON) 참조 - 근사치
    cursor.execute("SELECT id, question_ids FROM tests WHERE question_ids IS NOT NULL")
    for test_id, q_ids_json in cursor.fetchall():
        if q_ids_json:
            import json
            try:
                q_ids = json.loads(q_ids_json) if isinstance(q_ids_json, str) else q_ids_json
                for qid in question_ids:
                    if qid in q_ids:
                        refs["test_questions"] += 1
            except (json.JSONDecodeError, TypeError):
                pass

    return refs


def apply_dedup(cursor: sqlite3.Cursor, conn: sqlite3.Connection, groups: list[dict], delete: bool = False):
    """중복 제거 실행."""
    all_remove_ids = []
    for g in groups:
        all_remove_ids.extend(g["remove_ids"])

    if not all_remove_ids:
        print("제거할 중복 문제가 없습니다.")
        return

    # 참조 확인
    refs = check_references(cursor, all_remove_ids)
    if refs["answer_logs"] > 0:
        print(f"\n⚠ 주의: 제거 대상 중 {refs['answer_logs']}건이 answer_logs에 참조됨")
        print("  → 비활성화(is_active=0)로 처리합니다. (답안 기록 보존)")
        delete = False
    if refs["test_questions"] > 0:
        print(f"⚠ 주의: 제거 대상 중 {refs['test_questions']}건이 테스트에 포함됨")

    placeholders = ",".join("?" * len(all_remove_ids))

    if delete:
        cursor.execute(f"DELETE FROM questions WHERE id IN ({placeholders})", all_remove_ids)
        action = "삭제"
    else:
        cursor.execute(f"UPDATE questions SET is_active = 0 WHERE id IN ({placeholders})", all_remove_ids)
        action = "비활성화"

    conn.commit()
    print(f"\n✓ {len(all_remove_ids)}개 중복 문제 {action} 완료!")

    # 결과 확인
    cursor.execute("SELECT COUNT(*) FROM questions WHERE is_active = 1")
    remaining = cursor.fetchone()[0]
    print(f"  남은 활성 문제: {remaining}개")


def main():
    parser = argparse.ArgumentParser(description="중복 문제 탐지 및 제거")
    parser.add_argument("--apply", action="store_true", help="실제 제거 실행 (기본: 분석만)")
    parser.add_argument("--delete", action="store_true", help="비활성화 대신 완전 삭제")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"DB 파일을 찾을 수 없습니다: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 총 활성 문제 수
    cursor.execute("SELECT COUNT(*) FROM questions WHERE is_active = 1")
    total_active = cursor.fetchone()[0]

    # 중복 탐지
    groups = find_duplicates(cursor)

    if not groups:
        print("중복 문제가 없습니다!")
        conn.close()
        return

    # 보고서 출력
    print_report(groups, total_active)

    if args.apply:
        apply_dedup(cursor, conn, groups, delete=args.delete)
    else:
        total_remove = sum(len(g["remove_ids"]) for g in groups)
        print(f"\n※ 분석 모드입니다. 실제 제거하려면:")
        print(f"   python scripts/dedup_questions.py --apply          (비활성화)")
        print(f"   python scripts/dedup_questions.py --apply --delete (완전 삭제)")

    conn.close()


if __name__ == "__main__":
    main()
