from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from passlib.context import CryptContext

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse

from schemas.chats import ChatResponse
from models.chats import ChatHistory

router_user = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# CREATE ------------------------------------------------
@router_user.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # Kiểm tra email đã tồn tại chưa
    result = await db.execute(select(User).where(User.email == body.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(body.password)
    new_user = User(
        email=body.email,
        full_name=body.full_name,
        hashed_password=hashed_password,
        is_active=True,
        role="user",
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# GET LIST ---------------------------------------------
@router_user.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# GET ONE ----------------------------------------------
@router_user.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# UPDATE ------------------------------------------------
@router_user.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Cập nhật các trường nếu có trong body
    update_data = body.model_dump(exclude_unset=True)

    if "password" in update_data:
        hashed_password = pwd_context.hash(update_data["password"])
        user.hashed_password = hashed_password

    for key, value in update_data.items():
        if key != "password":
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

# DELETE ------------------------------------------------
@router_user.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    relust = await db.execute(select().where(User.id == user_id))
    user = relust.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}

@router_user.get("/chat_history/{user_id}", response_model=ChatResponse, status_code=200)
async def get_user_chat_history(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    relust = await db.execute(select(ChatHistory).where(ChatHistory.user_id == user_id)).order_by(ChatHistory.created_at.desc()).limited(10)
    chat_hitory = relust.scalar().all()
    if not chat_hitory:
        raise HTTPException(status_code=404, detail="User not found")
    
    return chat_hitory