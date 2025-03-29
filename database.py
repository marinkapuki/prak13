from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Создание асинхронного двигателя
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики асинхронных сессий
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

# Генератор для получения сессии базы данных
async def get_db() -> AsyncGenerator:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

