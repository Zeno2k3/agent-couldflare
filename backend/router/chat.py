from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from uuid import UUID


router_chat = APIRouter(prefix="/chat", tags=["Chats"])
from schemas.chats import ChatResponse, ChatCreate, ChatUpdate

from models.chats import ChatHistory
from models.user import User

from database import get_db

# Kiểm tra user đã đăng nhập chưa
# async def get_current_user_id() -> int:
# pass

@router_chat.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat ( body: ChatCreate, db: AsyncSession = Depends(get_db)):
 
 new_chat = ChatHistory(
  user_id=body.user_id,
  title=body.title,
 )
 db.add(new_chat)
 try:
  await db.commit()
  await db.refresh(new_chat)
  return new_chat
 except IntegrityError:
  await db.rollback()
  raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is invalid or other data constraint failed")


@router_chat.get("/",response_model=list[ChatResponse],status_code=status.HTTP_200_OK)
async def get_chats(user_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
 result = await db.execute(select(User).where(User.id == user_id))
 user = result.scalar_one_or_none()
 if not user:
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
 result = await db.execute(select(ChatHistory).where(ChatHistory.user_id == user_id).offset(skip).limit(limit).order_by(ChatHistory.created_at.desc()))
 return result.scalars().all()

@router_chat.delete("/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat(chat_id: UUID, db: AsyncSession = Depends(get_db)):
 
 chat_id = chat_id.hex
 result = await db.execute(select(ChatHistory).where(ChatHistory.id == chat_id))

 chat_history = result.scalar_one_or_none()
 if not chat_history:
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
 await db.delete(chat_history)
 await db.commit()
 return {"message": "Chat deleted successfully"}

@router_chat.put("/{chat_id}", response_model=ChatResponse, status_code=200)
async def update_chat(chat_id: UUID, body: ChatUpdate, db: AsyncSession = Depends(get_db)):
  chat_id = chat_id.hex
  result = await db.execute(select(ChatHistory).where(ChatHistory.id == chat_id))
  chat = result.scalar_one_or_none()
  if not chat:
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
  if chat.title != body.title:
    chat.title = body.title
    await db.commit()
    await db.refresh(chat)
  return chat