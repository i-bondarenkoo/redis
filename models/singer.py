from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class SingerOrm(Base):
    __tablename__ = "singers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    albums_count: Mapped[int] = mapped_column(Integer)
