from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import logging
import os

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

# ------------------------------------------------------------------
# 1. Tạo async engine (kết nối đến PostgreSQL/MySQL/SQLite qua async)
# ------------------------------------------------------------------

engine_sync = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
)

# ------------------------------------------------------------------
# 2. Tạo async session factory (dùng trong dependency injection)
# ------------------------------------------------------------------

async_session = async_sessionmaker(
    bind=engine_sync,  
    class_=AsyncSession,
    expire_on_commit=False, 
    autoflush=False,
    autocommit=False
)

# ------------------------------------------------------------------
# 3. Dependency để inject vào các router (get_db)
#    Dùng trong routers: db: AsyncSession = Depends(get_db)
# ------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection cho FastAPI.
    Mỗi request sẽ có 1 session riêng, tự động close khi xong.
    """
    async with async_session as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()         # Có lỗi thì rollback
            logging.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()           # Luôn luôn đóng session
