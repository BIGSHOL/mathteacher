"""Railway DB 비밀번호 해시 확인"""
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

cursor.execute("""
    SELECT login_id, hashed_password, role, is_active
    FROM users
    ORDER BY created_at;
""")

users = cursor.fetchall()
print(f"\n총 {len(users)}명의 사용자:")
print("-" * 80)
for user in users:
    print(f"login_id: {user[0]}")
    print(f"  hashed_password: {user[1][:60]}...")
    print(f"  role: {user[2]}")
    print(f"  is_active: {user[3]}")
    print()

cursor.close()
conn.close()
