from datetime import datetime

from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column

from imager_bot.database.models.base import Base


class UsersStatistics(Base):
    __tablename__ = "user_statistics"

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    start_date: Mapped[datetime] = mapped_column(types.DateTime, nullable=False)
    last_message_date: Mapped[datetime] = mapped_column(types.DateTime, nullable=False)
    start_message_count: Mapped[int] = mapped_column(types.Integer, default=0)
    screenshot_message_count: Mapped[int] = mapped_column(types.Integer, default=0)
    bad_request_count: Mapped[int] = mapped_column(types.Integer, default=0)
