from datetime import datetime

from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from imager_bot.database.models.base import Base
from imager_bot.database.models.roles import Roles


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    start_date: Mapped[datetime] = mapped_column(types.DateTime, nullable=False)
    last_message_date: Mapped[datetime] = mapped_column(types.DateTime, nullable=False)
    locale: Mapped[str] = mapped_column(types.String(2), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    role: Mapped["Roles"] = relationship(back_populates="users")
