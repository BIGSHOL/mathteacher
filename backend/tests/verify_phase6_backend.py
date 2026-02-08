import asyncio
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal, get_db
from app.services.daily_test_service import DailyTestService
from app.models.concept import Concept
from app.models.user import User
from sqlalchemy import select

async def test_randomized_generation():
    # DB 없이 로직만 테스트
    from app.schemas.common import ConceptMethod
    import random

    class MockService:
        def _pick_random_concept_method(self) -> str:
            r = random.random()
            if r < 0.4:
                return ConceptMethod.STANDARD
            elif r < 0.6:
                return ConceptMethod.GRADUAL_FADING
            elif r < 0.8:
                return ConceptMethod.ERROR_ANALYSIS
            else:
                return ConceptMethod.VISUAL_DECODING

    service = MockService()
    
    # _pick_random_concept_method 여러 번 호출해서 분포 확인
    counts = {}
    for _ in range(1000):
        m = service._pick_random_concept_method()
        counts[m] = counts.get(m, 0) + 1
    
    print("\n[Concept Method Distribution (1000 trials)]")
    for m, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {m}: {count/10:.1f}%")

if __name__ == "__main__":
    asyncio.run(test_randomized_generation())
