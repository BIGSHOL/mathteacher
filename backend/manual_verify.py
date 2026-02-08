
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.services.stats_service import StatsService
from app.services.ai_learning_service import AiLearningService

# Use memory-only SQLite for verification
engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def verify():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Given: Setup data
        student = User(id="s1", login_id="s1", name="S1", role="student", hashed_password="pw")
        concept = Concept(id="c1", name="C1", grade="middle_1", category="concept", part="algebra")
        db.add_all([student, concept])
        await db.commit()

        mastery = ConceptMastery(student_id="s1", concept_id="c1", mastery_percentage=75)
        db.add(mastery)
        await db.commit()

        # When: Test StatsService
        print("\n--- Verifying StatsService ---")
        stats_service = StatsService(db)
        radar_data = await stats_service.get_weak_concepts_radar("s1")
        print(f"Radar Data: {radar_data}")
        assert len(radar_data) == 1
        assert radar_data[0]["subject"] == "C1"
        assert radar_data[0]["score"] == 75

        # When: Test AiLearningService
        print("\n--- Verifying AiLearningService ---")
        ai_service = AiLearningService(db)
        weaknesses = await ai_service.analyze_weaknesses("s1")
        print(f"Weaknesses: {weaknesses}")
        assert len(weaknesses) == 1
        assert weaknesses[0]["concept_id"] == "c1"
        assert weaknesses[0]["mastery_score"] == 75

    print("\nVerification successful!")

if __name__ == "__main__":
    asyncio.run(verify())
