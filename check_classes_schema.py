"""classes 테이블 스키마 확인"""
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
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'classes'
    ORDER BY ordinal_position;
""")

columns = cursor.fetchall()
print("classes 테이블 컬럼:")
for col in columns:
    print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")

cursor.close()
conn.close()
