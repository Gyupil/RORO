from sqlalchemy import Column, Integer, Float, DateTime, func
from .database import Base

class IndexLog(Base):
    __tablename__ = "index_logs"

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    total_index = Column(Float)
    performance_index = Column(Float)
    fandom_index = Column(Float)
    buzz_index = Column(Float)