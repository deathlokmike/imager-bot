import asyncio

from sqlalchemy import text

from imager_bot.database.config import async_session


async def check_and_insert_roles():
    async with async_session() as session:
        query = text("SELECT * FROM roles")
        result = await session.execute(query)
        if len(result.scalars().all()) == 0:
            query = text("INSERT INTO roles (id, name) VALUES (0, 'User'), (1, 'Admin');")
            await session.execute(query)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(check_and_insert_roles())