from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Measurement(Base):
    __tablename__ = "measurements"
    id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[float]
    source: Mapped[str]
    date: Mapped[datetime]
