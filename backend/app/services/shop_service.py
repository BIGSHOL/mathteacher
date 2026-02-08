from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.item import Item, UserItem
from app.models.user import User


class ShopService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self, type: str | None = None) -> list[Item]:
        """구매 가능한 아이템 목록을 조회합니다."""
        query = select(Item).where(Item.is_active == True)
        if type:
            query = query.where(Item.type == type)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def list_inventory(self, user_id: str, type: str | None = None) -> list[UserItem]:
        """사용자가 보유한 아이템 목록을 조회합니다."""
        query = select(UserItem).options(selectinload(UserItem.item)).where(UserItem.user_id == user_id)
        
        if type:
            # Join을 통해 Item 타입 필터링
            query = query.join(Item).where(Item.type == type)
            
        result = await self.db.execute(query)
        return result.scalars().all()

    async def purchase_item(self, user_id: str, item_id: str) -> UserItem:
        """아이템을 구매합니다. XP가 차감됩니다."""
        # 1. 아이템 확인
        item = await self.db.get(Item, item_id)
        if not item or not item.is_active:
            raise HTTPException(status_code=404, detail="Item not found")

        # 2. 보유 여부 확인
        existing = await self.db.execute(
            select(UserItem).where(UserItem.user_id == user_id, UserItem.item_id == item_id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Already owned this item")

        # 3. 유저 XP 확인
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if user.total_xp < item.price:
            raise HTTPException(status_code=400, detail=f"Insufficient XP. Need {item.price} XP.")

        # 4. 구매 처리 (XP 차감 및 아이템 지급)
        user.total_xp -= item.price
        
        user_item = UserItem(user_id=user_id, item_id=item_id)
        self.db.add(user_item)
        
        # 즉시 장착? 일단 구매만.
        
        await self.db.commit()
        await self.db.refresh(user_item)
        
        # 관계 로드해서 반환
        return await self.db.get(UserItem, user_item.id, options=[selectinload(UserItem.item)])

    async def equip_item(self, user_id: str, item_id: str) -> UserItem:
        """아이템을 장착합니다. 같은 타입의 다른 아이템은 장착 해제됩니다."""
        # 1. 보유 아이템 확인 (Item 정보 포함 로드)
        query = select(UserItem).options(selectinload(UserItem.item)).where(
            UserItem.user_id == user_id, 
            UserItem.item_id == item_id
        )
        result = await self.db.execute(query)
        user_item = result.scalar_one_or_none()
        
        if not user_item:
            raise HTTPException(status_code=404, detail="You do not own this item")

        item_type = user_item.item.type

        # 2. 같은 타입의 다른 아이템 장착 해제
        # 서브쿼리나 조인을 사용하여 같은 타입의 장착된 아이템 조회
        
        # 먼저 해당 유저의 같은 타입 아이템 중 장착된 것들을 찾아서 해제
        # (비효율적일 수 있으나 명확하게 처리)
        equipped_query = select(UserItem).join(Item).where(
            UserItem.user_id == user_id,
            UserItem.is_equipped == True,
            Item.type == item_type
        )
        equipped_result = await self.db.execute(equipped_query)
        current_equipped = equipped_result.scalars().all()
        
        for item in current_equipped:
            item.is_equipped = False
            
        # 3. 대상 아이템 장착
        user_item.is_equipped = True
        
        await self.db.commit()
        await self.db.refresh(user_item)
        return user_item

    async def unequip_item(self, user_id: str, item_id: str) -> UserItem:
        """아이템 장착을 해제합니다."""
        user_item = await self.db.get(UserItem, item_id) # 주의: item_id가 아니라 user_item_id인지 확인 필요. 여기선 item_id를 받아서 처리
        # API 설계 상 item_id를 받는게 직관적일 수 있음. 
        # 하지만 purchase_item이 item_id를 받으므로, equip도 item_id를 받는게 맞음.
        
        query = select(UserItem).where(
            UserItem.user_id == user_id,
            UserItem.item_id == item_id
        )
        result = await self.db.execute(query)
        user_item = result.scalar_one_or_none()
        
        if not user_item:
            raise HTTPException(status_code=404, detail="Item not owned")
            
        user_item.is_equipped = False
        await self.db.commit()
        return user_item
