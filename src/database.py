from typing import TypeVar

import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql._typing import ColumnExpressionArgument

from .models import Base

DatabaseModel = Base
T_DatabaseModel = TypeVar("T_DatabaseModel", bound=Base)

_engine = create_async_engine("sqlite+aiosqlite:///data/bot.db")
_sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)


class Database:
    engine = _engine
    sessionmaker = _sessionmaker

    @classmethod
    async def close(cls) -> None:
        """Close the database, should be called once before closing."""
        await cls.engine.dispose()

    @classmethod
    async def insert_or_replace(cls, instance: DatabaseModel) -> None:
        """Insert an object into the database. If an object with the same Primary Key already exists,
        replace it with the new object.

        Example: `Database.insert_or_replace(User(discord_id=123))`

        Parameters:
        ------
        instance: `DatabaseModel`
            An instance object of the database Table (ORM).
        """
        async with cls.sessionmaker() as session:
            await session.merge(instance)
            await session.commit()

    @classmethod
    async def select_one(
        cls,
        table: type[T_DatabaseModel],
        whereclause: ColumnExpressionArgument[bool] | None = None,
    ) -> T_DatabaseModel | None:
        """Select one object from the database table based on the specified conditions.

        Example: `Database.select_one(User, User.discord_id.is_(id))`

        Parameters
        ------
        table: `type[T_DatabaseModel]`
            The class of the database Table (ORM) to select from. Ex: `User`.
        whereclause: `ColumnExpressionArgument[bool]` | `None`
            Where clause condition based on ORM Column. Ex: `User.discord_id.is_(123456)`.

        Returns
        ------
        `T_DatabaseModel` | `None`:
            The object from the specified Table that satisfies the conditions,
            or `None` if no object satisfies the conditions.
        """
        async with cls.sessionmaker() as session:
            stmt = sqlalchemy.select(table)
            if whereclause is not None:
                stmt = stmt.where(whereclause)
            result = await session.execute(stmt)
            return result.scalar()
