from sqlalchemy.orm import Mapped, relationship, mapped_column
from models.base import Base
from models.type import str_idx, str_pk, timestamp, updated_timestamp
from sqlalchemy import ForeignKey, String
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID 

class ChatHistory(Base):
 __tablename__ = "chat_histories"
 id: Mapped[String] = mapped_column(String(36), primary_key=True, default=uuid4)
 user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
 title: Mapped[str_idx]
 created_at: Mapped[timestamp]
 updated_at: Mapped[updated_timestamp]

 user: Mapped["User"] = relationship(back_populates="chat_histories")

