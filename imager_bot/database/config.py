from loguru import logger
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from imager_bot.config import settings

db_params = {}

if settings.MODE in ["TEST", "DEV"]:
    db_url = f"postgresql+asyncpg://{settings.get_test_database_url}"
    if settings.MODE == "TEST":
        db_params["poolclass"] = NullPool
else:
    db_url = f"postgresql+asyncpg://{settings.get_database_url}"
logger.debug(f"Init async engine [{db_params}]")
engine = create_async_engine(db_url, **db_params)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
