"""Railway DB 사용자 확인"""
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

# 모든 사용자 조회
cursor.execute("""
    SELECT id, login_id, name, role, grade, is_active
    FROM users
    ORDER BY created_at;
""")

users = cursor.fetchall()
print(f"\n총 {len(users)}명의 사용자:")
print("-" * 80)
for user in users:
    print(f"ID: {user[0]}")
    print(f"  login_id: {user[1]}")
    print(f"  name: {user[2]}")
    print(f"  role: {user[3]}")
    print(f"  grade: {user[4]}")
    print(f"  is_active: {user[5]}")
    print()

cursor.close()
conn.close()
