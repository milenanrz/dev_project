import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

load_dotenv()
DB=(
    f"postgresql+asyncpg://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT','5432')}/{os.getenv('DATABASE')}"
)

DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine : AsyncEngine = create_async_engine(DB, echo=True)
async_session =sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session