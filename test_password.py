"""비밀번호 해시 검증 테스트"""
import bcrypt

# DB에 저장된 해시
stored_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7w9T9Hkjr2"

# 테스트할 비밀번호들
test_passwords = [
    "password123",
    "Password123",
    "password",
    "123",
]

print("비밀번호 해시 검증 테스트:")
print(f"저장된 해시: {stored_hash}")
print("-" * 80)

for pwd in test_passwords:
    try:
        result = bcrypt.checkpw(pwd.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f"'{pwd}': {result}")
    except Exception as e:
        print(f"'{pwd}': ERROR - {e}")

# 새로운 해시 생성 테스트
print("\n" + "-" * 80)
print("password123으로 새 해시 생성:")
new_hash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
print(f"새 해시: {new_hash.decode('utf-8')}")
print(f"검증: {bcrypt.checkpw('password123'.encode('utf-8'), new_hash)}")
