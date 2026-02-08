
import sys
from pydantic import TypeAdapter
from app.schemas.stats import StudentStats

print("Import successful")
try:
    print("Generating schema for StudentStats...")
    adapter = TypeAdapter(StudentStats)
    schema = adapter.json_schema()
    print("Schema generation successful")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
sys.exit(0)
