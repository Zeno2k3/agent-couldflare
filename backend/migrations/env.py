# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine
import asyncio

from alembic import context

# Import Base từ models của bạn
from models.base import Base

# this is the Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata cho autogenerate
target_metadata = Base.metadata


def get_url():
    """Lấy URL từ config, hoặc từ env nếu cần override"""
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ offline"""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Các option hữu ích
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Chạy migration ở chế độ online với async engine"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    # Cách đúng để tạo AsyncEngine trong Alembic
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    """Hàm sync được gọi bên trong async context"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,  # Quan trọng nếu dùng SQLite!
        # version_table_schema="your_schema" nếu cần
    )

    with context.begin_transaction():
        context.run_migrations()


# Chọn chế độ chạy
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())