"""올바른 비밀번호 해시로 재설정"""
import psycopg2
from urllib.parse import urlparse
import bcrypt

DATABASE_URL = "postgresql://postgres:vODSnuVJqSJRiTJdzVmVpnvdNQqjaHGU@switchback.proxy.rlwy.net:24110/railway"

# 올바른 해시 생성 (백엔드와 동일한 방식)
password = "password123"
correct_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

print(f"[INFO] 새 해시 생성: {correct_hash}")
print(f"[INFO] 검증: {bcrypt.checkpw(password.encode('utf-8'), correct_hash.encode('utf-8'))}")

result = urlparse(DATABASE_URL)
conn = psycopg2.connect(
    database=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)

cursor = conn.cursor()

# 모든 사용자의 비밀번호를 올바른 해시로 업데이트
cursor.execute("""
    UPDATE users
    SET hashed_password = %s
    WHERE login_id IN ('master01', 'student01', 'student02', 'student03');
""", (correct_hash,))

affected = cursor.rowcount
conn.commit()

print(f"[OK] {affected}명의 비밀번호를 올바른 해시로 재설정했습니다.")

# 검증
cursor.execute("""
    SELECT login_id, hashed_password
    FROM users
    WHERE login_id IN ('master01', 'student01', 'student02', 'student03')
    ORDER BY login_id;
""")

users = cursor.fetchall()
print("\n[검증] 업데이트된 사용자:")
for user in users:
    print(f"  {user[0]}: {user[1][:60]}...")

cursor.close()
conn.close()

print("\n[SUCCESS] 비밀번호 재설정 완료!")
print("로그인 정보: master01 / password123")
