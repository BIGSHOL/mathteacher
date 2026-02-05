"""classes 테이블 grade 컬럼 VARCHAR로 변경"""
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
conn.autocommit = True
cursor = conn.cursor()

print("[1/2] classes 테이블 grade를 VARCHAR로 변경 중...")
try:
    cursor.execute("""
        ALTER TABLE classes
        ALTER COLUMN grade TYPE VARCHAR(20) USING grade::text;
    """)
    print("[OK] classes.grade -> VARCHAR(20)")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n[2/2] classes 테이블 grade 값을 소문자로 변경 중...")
try:
    cursor.execute("UPDATE classes SET grade = LOWER(grade);")
    print(f"[OK] classes.grade 소문자 변환: {cursor.rowcount}행")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n[SUCCESS] classes 테이블 수정 완료!")

cursor.close()
conn.close()
