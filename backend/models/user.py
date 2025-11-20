from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List, Optional
from .type import str_pk, str_unique, bool_default_true, bool_default_false

from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str_pk] 
    username: Mapped[str_unique]
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool_default_true]
    is_superuser: Mapped[bool_default_false]

    # Relationship
    # posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")