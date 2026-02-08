import asyncio
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.models.item import Item
from sqlalchemy import select

async def seed_items():
    async with AsyncSessionLocal() as db:
        # Check if items exist
        result = await db.execute(select(Item))
        if result.scalars().first():
            print("Items already exist. Skipping seed.")
            return

        items = [
            # Avatars
            Item(
                name="기본 아바타",
                type="avatar",
                description="기본적으로 제공되는 아바타입니다.",
                price=0,
                image_url="",
                is_active=True
            ),
            Item(
                name="고양이 아바타",
                type="avatar",
                description="귀여운 고양이 아바타입니다.",
                price=500,
                image_url="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
                is_active=True
            ),
            Item(
                name="로봇 아바타",
                type="avatar",
                description="멋진 미래형 로봇 아바타입니다.",
                price=1000,
                image_url="https://api.dicebear.com/7.x/bottts/svg?seed=Robot",
                is_active=True
            ),
            Item(
                name="마법사 아바타",
                type="avatar",
                description="신비로운 마법사 아바타입니다.",
                price=2000,
                image_url="https://api.dicebear.com/7.x/avataaars/svg?seed=Wizard&clothing=graphicShirt&clothingColor=262e33",
                is_active=True
            ),
            
            # Themes
            Item(
                name="다크 모드 테마",
                type="theme",
                description="눈이 편안한 다크 모드 테마입니다.",
                price=1500,
                image_url="",
                is_active=True
            ),
            Item(
                name="바다 테마",
                type="theme",
                description="시원한 바다 느낌의 테마입니다.",
                price=1200,
                image_url="",
                is_active=True
            ),
        ]

        db.add_all(items)
        await db.commit()
        print(f"Successfully added {len(items)} items.")

if __name__ == "__main__":
    asyncio.run(seed_items())
