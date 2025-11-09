# api/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# --- 스냅샷 응답용 스키마 ---
class IndexSnapshotResponse(BaseModel):
    total_index: float
    total_index_change_24h: float
    performance_index: float
    performance_index_change_24h: float
    fandom_index: float
    fandom_index_change_24h: float
    buzz_index: float
    buzz_index_change_24h: float


# --- 트렌드 차트 응답용 스키마 ---
class IndexTrendResponse(BaseModel):
    categories: List[str]  # X축 (날짜)
    performance_data: List[float]  # 성과 지수 시리즈
    fandom_data: List[float]  # 팬덤 지수 시리즈
    buzz_data: List[float]  # 버즈 지수 시리즈

    class Config:
        orm_mode = True  # SQLAlchemy 모델과 자동 매핑