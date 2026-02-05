"""Railway DB 비밀번호 재설정"""
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

# bcrypt 해시: password123
hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7w9T9Hkjr2"

# 모든 사용자의 비밀번호를 password123으로 재설정
cursor.execute("""
    UPDATE users
    SET hashed_password = %s
    WHERE login_id IN ('master01', 'student01', 'student02', 'student03');
""", (hashed_password,))

affected = cursor.rowcount
conn.commit()

print(f"[OK] {affected}명의 비밀번호를 password123으로 재설정했습니다.")

cursor.close()
conn.close()
