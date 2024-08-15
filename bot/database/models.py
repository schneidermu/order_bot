from database.base import Base
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, default=1)

    def __repr__(self):
        return f"UserModel(id={self.id!r}, username={self.username})"
