from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from imager_bot.database.models.base import Base

if TYPE_CHECKING:
    from imager_bot.database.models.users import Users


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[list["Users"]] = relationship(back_populates="role")
