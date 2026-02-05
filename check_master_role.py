"""마스터 계정 role 확인"""
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

# master01 계정의 모든 정보 확인
cursor.execute("""
    SELECT id, login_id, name, role, grade, is_active
    FROM users
    WHERE login_id = 'master01';
""")

user = cursor.fetchone()
if user:
    print("[마스터 계정 정보]")
    print(f"  ID: {user[0]}")
    print(f"  login_id: {user[1]}")
    print(f"  name: {user[2]}")
    print(f"  role: {user[3]} (type: {type(user[3]).__name__})")
    print(f"  grade: {user[4]}")
    print(f"  is_active: {user[5]}")
else:
    print("[ERROR] master01 계정을 찾을 수 없습니다.")

# role enum 값 확인
cursor.execute("""
    SELECT enumlabel FROM pg_enum
    WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')
    ORDER BY enumsortorder;
""")
enum_values = [row[0] for row in cursor.fetchall()]
print(f"\n[UserRole enum 값]: {enum_values}")

cursor.close()
conn.close()
