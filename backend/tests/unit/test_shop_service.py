
import pytest
from fastapi import HTTPException
from app.models.item import Item, UserItem
from app.models.user import User
from app.services.shop_service import ShopService

@pytest.mark.asyncio
async def test_purchase_item_success(db_session):
    """purchase_item: 성공 시 XP 차감 및 아이템 지급 확인"""
    # Given
    user = User(id="u_shop_1", login_id="u_shop_1", name="Shop User", role="student", hashed_password="pw", is_active=True, level=1, total_xp=1000)
    db_session.add(user)
    
    item = Item(id="item_1", name="Avatar 1", type="avatar", price=500, image_url="url", is_active=True)
    db_session.add(item)
    await db_session.commit()
    
    # When
    service = ShopService(db_session)
    user_item = await service.purchase_item(user.id, item.id)
    
    # Then
    assert user.total_xp == 500  # 1000 - 500
    assert user_item.item_id == "item_1"
    assert user_item.user_id == user.id

@pytest.mark.asyncio
async def test_purchase_item_insufficient_xp(db_session):
    """purchase_item: XP 부족 시 예외 발생 확인"""
    # Given
    user = User(id="u_shop_2", login_id="u_shop_2", name="Poor User", role="student", hashed_password="pw", is_active=True, level=1, total_xp=100)
    db_session.add(user)
    
    item = Item(id="item_2", name="Expensive Item", type="avatar", price=500, image_url="url", is_active=True)
    db_session.add(item)
    await db_session.commit()
    
    # When/Then
    service = ShopService(db_session)
    with pytest.raises(HTTPException) as excinfo:
        await service.purchase_item(user.id, item.id)
    assert excinfo.value.status_code == 400
    assert "Insufficient XP" in excinfo.value.detail

@pytest.mark.asyncio
async def test_purchase_item_already_owned(db_session):
    """purchase_item: 이미 보유한 아이템 구매 시 예외 발생 확인"""
    # Given
    user = User(id="u_shop_3", login_id="u_shop_3", name="User", role="student", hashed_password="pw", is_active=True, level=1, total_xp=1000)
    db_session.add(user)
    
    item = Item(id="item_3", name="My Item", type="avatar", price=100, image_url="url", is_active=True)
    db_session.add(item)
    
    user_item = UserItem(user_id=user.id, item_id=item.id)
    db_session.add(user_item)
    await db_session.commit()
    
    # When/Then
    service = ShopService(db_session)
    with pytest.raises(HTTPException) as excinfo:
        await service.purchase_item(user.id, item.id)
    assert excinfo.value.status_code == 400
    assert "Already owned" in excinfo.value.detail

@pytest.mark.asyncio
async def test_equip_item_swaps_same_type(db_session):
    """equip_item: 같은 타입 아이템 자동 해제 및 새 아이템 장착 확인"""
    # Given
    user = User(id="u_shop_4", login_id="u_shop_4", name="User", role="student", hashed_password="pw", is_active=True, level=1, total_xp=1000)
    db_session.add(user)
    
    item1 = Item(id="avatar_1", name="Avatar 1", type="avatar", price=100, image_url="url", is_active=True)
    item2 = Item(id="avatar_2", name="Avatar 2", type="avatar", price=100, image_url="url", is_active=True)
    db_session.add_all([item1, item2])
    
    # item1 equipped
    ui1 = UserItem(user_id=user.id, item_id="avatar_1", is_equipped=True)
    ui2 = UserItem(user_id=user.id, item_id="avatar_2", is_equipped=False)
    db_session.add_all([ui1, ui2])
    await db_session.commit()
    
    # When: Equip item2
    service = ShopService(db_session)
    result = await service.equip_item(user.id, "avatar_2")
    
    # Then
    await db_session.refresh(ui1)
    await db_session.refresh(ui2)
    
    assert result.item_id == "avatar_2"
    assert ui2.is_equipped is True
    assert ui1.is_equipped is False
