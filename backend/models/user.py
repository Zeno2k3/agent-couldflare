from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List, Optional
from models.type import str_pk, str_unique, bool_default_true, timestamp, updated_timestamp

from models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str_pk] 
    email: Mapped[str_unique]
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="user")
    is_active: Mapped[bool_default_true]
    created_at: Mapped[timestamp] 
    updated_at: Mapped[updated_timestamp]
    # Relationship
    # posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")