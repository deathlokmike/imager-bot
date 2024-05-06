from sqlalchemy import types
from sqlalchemy.orm import mapped_column, Mapped

from imager_bot.database.models.base import Base


class UsersStatistics(Base):
    __tablename__ = "user_statistics"

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    start_message_count: Mapped[int] = mapped_column(types.Integer, default=0)
    screenshot_message_count: Mapped[int] = mapped_column(types.Integer, default=0)
    bad_request_count: Mapped[int] = mapped_column(types.Integer, default=0)
