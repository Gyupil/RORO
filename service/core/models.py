from sqlalchemy import Column, Integer, Float, DateTime, func, Identity
from .database import Base

class IndexLog(Base):
    __tablename__ = "index_logs"

    id = Column(Integer, Identity(), primary_key=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    total_index = Column(Float)
    performance_index = Column(Float)
    fandom_index = Column(Float)
    buzz_index = Column(Float)