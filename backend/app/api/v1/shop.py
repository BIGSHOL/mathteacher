from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.shop_service import ShopService

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("/items")
async def get_shop_items(
    type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """구매 가능한 상점 아이템 목록을 조회합니다."""
    service = ShopService(db)
    items = await service.list_items(type)
    return {"success": True, "data": items}


@router.get("/inventory")
async def get_my_inventory(
    type: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """내 인벤토리를 조회합니다."""
    service = ShopService(db)
    inventory = await service.list_inventory(current_user.id, type)
    
    # 필요한 데이터만 정제해서 반환 (API 응답 스키마 필요 시 추가 정의)
    data = []
    for entry in inventory:
        data.append({
            "id": entry.item.id, # 아이템 ID
            "name": entry.item.name,
            "type": entry.item.type,
            "image_url": entry.item.image_url,
            "price": entry.item.price,
            "purchased_at": entry.purchased_at,
            "is_equipped": entry.is_equipped,
            "user_item_id": entry.id
        })
        
    return {"success": True, "data": data}


@router.post("/purchase/{item_id}")
async def purchase_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """아이템을 구매합니다."""
    service = ShopService(db)
    user_item = await service.purchase_item(current_user.id, item_id)
    return {"success": True, "message": "Item purchased successfully", "data": {
        "user_item_id": user_item.id,
        "balance_xp": current_user.total_xp # 갱신된 XP 정보 반환
    }}


@router.post("/equip/{item_id}")
async def equip_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """아이템을 장착합니다. (같은 타입의 기존 아이템은 자동 해제)"""
    service = ShopService(db)
    user_item = await service.equip_item(current_user.id, item_id)
    return {"success": True, "message": "Item equipped successfully", "data": {
        "is_equipped": user_item.is_equipped
    }}


@router.post("/unequip/{item_id}")
async def unequip_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """아이템 장착을 해제합니다."""
    service = ShopService(db)
    await service.unequip_item(current_user.id, item_id)
    return {"success": True, "message": "Item unequipped successfully"}
