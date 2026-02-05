"""PostgreSQL enum을 VARCHAR로 변경"""
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = "postgresql://postgres:vODSnuVJqSJRiTJdzVmVpnvdNQqjaHGU@switchback.proxy.rlwy.net:24110/railway"

result = urlparse(DATABASE_URL)
conn = psycopg2.connect(
    database=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)

cursor = conn.cursor()

print("[1/4] UserRole enum을 VARCHAR로 변경 중...")
# users 테이블의 role을 VARCHAR로 변경
cursor.execute("""
    ALTER TABLE users
    ALTER COLUMN role TYPE VARCHAR(20) USING role::text;
""")
print("[OK] users.role → VARCHAR(20)")

print("\n[2/4] Grade enum을 VARCHAR로 변경 중...")
# users 테이블의 grade를 VARCHAR로 변경
cursor.execute("""
    ALTER TABLE users
    ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
""")
print("[OK] users.grade → VARCHAR(20)")

# chapters 테이블의 grade를 VARCHAR로 변경
cursor.execute("""
    ALTER TABLE chapters
    ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
""")
print("[OK] chapters.grade → VARCHAR(20)")

# tests 테이블의 grade를 VARCHAR로 변경
cursor.execute("""
    ALTER TABLE tests
    ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
""")
print("[OK] tests.grade → VARCHAR(20)")

# concepts 테이블의 grade를 VARCHAR로 변경
cursor.execute("""
    ALTER TABLE concepts
    ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
""")
print("[OK] concepts.grade → VARCHAR(20)")

# questions 테이블의 grade를 VARCHAR로 변경 (있다면)
try:
    cursor.execute("""
        ALTER TABLE questions
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] questions.grade → VARCHAR(20)")
except:
    print("  (questions.grade 컬럼 없음 - 스킵)")

print("\n[3/4] Enum 타입 삭제 중...")
# enum 타입 삭제 (이제 사용하지 않음)
try:
    cursor.execute("DROP TYPE IF EXISTS userrole CASCADE;")
    print("[OK] userrole enum 삭제")
except Exception as e:
    print(f"  userrole enum 삭제 실패: {e}")

try:
    cursor.execute("DROP TYPE IF EXISTS grade CASCADE;")
    print("[OK] grade enum 삭제")
except Exception as e:
    print(f"  grade enum 삭제 실패: {e}")

print("\n[4/4] 데이터 값을 소문자로 변경 중...")
# 모든 role 값을 소문자로 변경
cursor.execute("""
    UPDATE users SET role = LOWER(role);
""")
print(f"[OK] users.role 소문자 변환: {cursor.rowcount}행")

# 모든 grade 값을 소문자로 변경
cursor.execute("""
    UPDATE users SET grade = LOWER(grade) WHERE grade IS NOT NULL;
""")
print(f"[OK] users.grade 소문자 변환: {cursor.rowcount}행")

cursor.execute("""
    UPDATE chapters SET grade = LOWER(grade);
""")
print(f"[OK] chapters.grade 소문자 변환: {cursor.rowcount}행")

cursor.execute("""
    UPDATE tests SET grade = LOWER(grade);
""")
print(f"[OK] tests.grade 소문자 변환: {cursor.rowcount}행")

cursor.execute("""
    UPDATE concepts SET grade = LOWER(grade);
""")
print(f"[OK] concepts.grade 소문자 변환: {cursor.rowcount}행")

conn.commit()

print("\n" + "="*60)
print("[SUCCESS] Enum 제거 완료!")
print("="*60)
print("\n이제 백엔드 모델도 VARCHAR로 변경하고, enum 값을 소문자로 되돌려야 합니다.")

cursor.close()
conn.close()
