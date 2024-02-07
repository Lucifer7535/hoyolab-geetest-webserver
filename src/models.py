import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for database tables, inherits from sqlalchemy `MappedAsDataclass`, `DeclarativeBase`"""

    type_annotation_map = {dict[str, str]: sqlalchemy.JSON}


class User(Base):
    """User database table"""

    __tablename__ = "users"

    discord_id: Mapped[int] = mapped_column(primary_key=True)
    """User Discord ID"""


class GeetestChallenge(Base):
    """Table for storing Geetest challenge values used in sign-in graphics verification"""

    __tablename__ = "geetest_challenge"

    discord_id: Mapped[int] = mapped_column(primary_key=True)
    """User Discord ID"""

    genshin: Mapped[dict[str, str] | None] = mapped_column(default=None)
    """Genshin challenge value"""
    honkai3rd: Mapped[dict[str, str] | None] = mapped_column(default=None)
    """Honkai3rd challenge value"""
    starrail: Mapped[dict[str, str] | None] = mapped_column(default=None)
