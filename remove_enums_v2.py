"""PostgreSQL enum을 VARCHAR로 변경 (트랜잭션 분리)"""
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
conn.autocommit = True  # 자동 커밋 모드
cursor = conn.cursor()

print("[1/5] UserRole enum을 VARCHAR로 변경 중...")
try:
    cursor.execute("""
        ALTER TABLE users
        ALTER COLUMN role TYPE VARCHAR(20) USING role::text;
    """)
    print("[OK] users.role -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] users.role: {e}")

print("\n[2/5] Grade enum을 VARCHAR로 변경 중...")
try:
    cursor.execute("""
        ALTER TABLE users
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] users.grade -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] users.grade: {e}")

try:
    cursor.execute("""
        ALTER TABLE chapters
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] chapters.grade -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] chapters.grade: {e}")

try:
    cursor.execute("""
        ALTER TABLE tests
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] tests.grade -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] tests.grade: {e}")

try:
    cursor.execute("""
        ALTER TABLE concepts
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] concepts.grade -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] concepts.grade: {e}")

print("\n[3/5] Enum 타입 삭제 중...")
try:
    cursor.execute("DROP TYPE IF EXISTS userrole CASCADE;")
    print("[OK] userrole enum 삭제")
except Exception as e:
    print(f"[SKIP] userrole: {e}")

try:
    cursor.execute("DROP TYPE IF EXISTS grade CASCADE;")
    print("[OK] grade enum 삭제")
except Exception as e:
    print(f"[SKIP] grade: {e}")

print("\n[4/5] 데이터 값을 소문자로 변경 중...")
try:
    cursor.execute("UPDATE users SET role = LOWER(role);")
    print(f"[OK] users.role 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] users.role: {e}")

try:
    cursor.execute("UPDATE users SET grade = LOWER(grade) WHERE grade IS NOT NULL;")
    print(f"[OK] users.grade 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] users.grade: {e}")

try:
    cursor.execute("UPDATE chapters SET grade = LOWER(grade);")
    print(f"[OK] chapters.grade 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] chapters.grade: {e}")

try:
    cursor.execute("UPDATE tests SET grade = LOWER(grade);")
    print(f"[OK] tests.grade 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] tests.grade: {e}")

try:
    cursor.execute("UPDATE concepts SET grade = LOWER(grade);")
    print(f"[OK] concepts.grade 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] concepts.grade: {e}")

print("\n[5/5] 결과 확인...")
cursor.execute("SELECT login_id, role, grade FROM users ORDER BY login_id LIMIT 5;")
users = cursor.fetchall()
for user in users:
    print(f"  {user[0]}: role={user[1]}, grade={user[2]}")

print("\n" + "="*60)
print("[SUCCESS] Enum 제거 완료!")
print("="*60)
print("\n다음 단계: 백엔드 모델에서 Enum 타입을 String으로 변경")

cursor.close()
conn.close()
