"""Railway DB에 사용자 생성 스크립트"""
import os
import psycopg2
from urllib.parse import urlparse
from datetime import datetime, timezone

# Railway DATABASE_URL
DATABASE_URL = "postgresql://postgres:vODSnuVJqSJRiTJdzVmVpnvdNQqjaHGU@switchback.proxy.rlwy.net:24110/railway"

# URL 파싱
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

print(f"[INFO] 연결 중: {hostname}:{port}/{database}")

# PostgreSQL 연결
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)

cursor = conn.cursor()

# 1. users 테이블 확인
cursor.execute("SELECT COUNT(*) FROM users;")
count = cursor.fetchone()[0]
print(f"[INFO] 현재 사용자 수: {count}")

# 1-1. enum 타입 확인
cursor.execute("""
    SELECT enumlabel FROM pg_enum
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')
    ORDER BY enumsortorder;
""")
enum_values = [row[0] for row in cursor.fetchall()]
print(f"[INFO] UserRole enum 값: {enum_values}")

cursor.execute("""
    SELECT enumlabel FROM pg_enum
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'grade')
    ORDER BY enumsortorder;
""")
grade_enum_values = [row[0] for row in cursor.fetchall()]
print(f"[INFO] Grade enum 값: {grade_enum_values}")

# 2. 마스터 계정 확인
cursor.execute("SELECT id, login_id, name, role FROM users WHERE login_id = 'master01';")
master = cursor.fetchone()
if master:
    print(f"[OK] 마스터 계정 존재: {master}")
else:
    print("[WARN] 마스터 계정 없음. 생성 중...")

    # bcrypt 해시: password123
    hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7w9T9Hkjr2"
    now = datetime.now(timezone.utc)

    cursor.execute("""
        INSERT INTO users (
            id, login_id, name, role, hashed_password, is_active,
            level, total_xp, current_streak, max_streak, level_down_defense,
            has_completed_placement,
            created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (
        "master-001",
        "master01",
        "마스터 관리자",
        "MASTER",
        hashed_password,
        True,
        1,  # level
        0,  # total_xp
        0,  # current_streak
        0,  # max_streak
        3,  # level_down_defense
        False,  # has_completed_placement
        now,
        now
    ))
    print("[OK] 마스터 계정 생성됨")

# 3. 학생 계정 확인 및 생성
students = [
    ("student-001", "student01", "테스트 학생1", "MIDDLE_1", None),
    ("student-002", "student02", "테스트 학생2", "ELEMENTARY_3", None),
    ("student-003", "student03", "테스트 학생3", "HIGH_1", None),
]

hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7w9T9Hkjr2"
now = datetime.now(timezone.utc)

for student_id, login_id, name, grade, class_id in students:
    cursor.execute("SELECT id FROM users WHERE login_id = %s;", (login_id,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("""
            INSERT INTO users (
                id, login_id, name, role, grade, class_id, hashed_password, is_active,
                level, total_xp, current_streak, max_streak, level_down_defense,
                has_completed_placement,
                created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            student_id,
            login_id,
            name,
            "STUDENT",
            grade,
            class_id,
            hashed_password,
            True,
            1,  # level
            0,  # total_xp
            0,  # current_streak
            0,  # max_streak
            3,  # level_down_defense
            False,  # has_completed_placement
            now,
            now
        ))
        print(f"[OK] 학생 계정 생성: {login_id}")
    else:
        print(f"[SKIP] 학생 계정 존재: {login_id}")

conn.commit()
cursor.close()
conn.close()

print("\n[SUCCESS] 사용자 생성 완료!")
print("\n로그인 계정:")
print("  master01 / password123")
print("  student01 / password123")
print("  student02 / password123")
print("  student03 / password123")
