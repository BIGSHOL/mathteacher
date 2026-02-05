"""단원 데이터 확인"""
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

# 단원 개수 확인
cursor.execute("SELECT COUNT(*) FROM chapters;")
chapter_count = cursor.fetchone()[0]
print(f"단원 개수: {chapter_count}")

# 학년별 단원 개수
cursor.execute("""
    SELECT grade, COUNT(*)
    FROM chapters
    GROUP BY grade
    ORDER BY grade;
""")
by_grade = cursor.fetchall()
print("\n학년별 단원:")
for grade, count in by_grade:
    print(f"  {grade}: {count}개")

# 샘플 단원 몇 개 확인
cursor.execute("""
    SELECT id, name, grade, semester, chapter_number
    FROM chapters
    ORDER BY grade, semester, chapter_number
    LIMIT 10;
""")
samples = cursor.fetchall()
print("\n샘플 단원:")
for ch in samples:
    print(f"  [{ch[2]}] {ch[3]}학기 {ch[4]}단원: {ch[1]}")

cursor.close()
conn.close()
