# api/services.py
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from service.core.models import IndexLog
from service.api.schema import IndexSnapshotResponse, IndexTrendResponse
from datetime import datetime, timedelta


def get_snapshot_data(db: Session) -> IndexSnapshotResponse:
    """
    가장 최신의 지수와 24시간 전 대비 변화량을 계산하여 반환합니다.
    (스냅샷 UI용)
    """
    latest_log = db.query(IndexLog).order_by(desc(IndexLog.created_at)).first()

    if not latest_log:
        # 데이터가 없을 경우 기본값 반환 (수정)
        return IndexSnapshotResponse(
            total_index=0, total_index_change_24h=0,
            performance_index=0, performance_index_change_24h=0,
            fandom_index=0, fandom_index_change_24h=0,
            buzz_index=0, buzz_index_change_24h=0
        )

    # 24시간 전 데이터 조회 (근사치)
    time_24h_ago = latest_log.created_at - timedelta(days=1)
    prev_log = db.query(IndexLog) \
        .filter(IndexLog.created_at <= time_24h_ago) \
        .order_by(desc(IndexLog.created_at)) \
        .first()

    # 변화량 기본값 (24시간 전 데이터가 없을 경우)
    total_change = 0
    perf_change = 0
    fand_change = 0
    buzz_change = 0

    if prev_log:
        # 24시간 전 데이터가 있으면 변화량 계산
        total_change = latest_log.total_index - prev_log.total_index
        perf_change = latest_log.performance_index - prev_log.performance_index
        fand_change = latest_log.fandom_index - prev_log.fandom_index
        buzz_change = latest_log.buzz_index - prev_log.buzz_index

    return IndexSnapshotResponse(
        total_index=latest_log.total_index,
        total_index_change_24h=round(total_change, 2),
        performance_index=latest_log.performance_index,
        performance_index_change_24h=round(perf_change, 2),  # 추가
        fandom_index=latest_log.fandom_index,
        fandom_index_change_24h=round(fand_change, 2),  # 추가
        buzz_index=latest_log.buzz_index,
        buzz_index_change_24h=round(buzz_change, 2)  # 추가
    )


def get_trend_data(db: Session, days: int = 30) -> IndexTrendResponse:
    """
    최근 N일간의 지수 트렌드 데이터를 차트 형식에 맞게 반환합니다.
    (X축 중복 문제를 해결하도록 로직 수정)
    """

    # 1. 요청된 기간에 따라 시작 날짜 결정
    if days == 1:  # 24시간
        start_date = datetime.now() - timedelta(days=1)
        default_format_str = '%H:%M'  # '시:분'
    elif days <= 7:  # 7일
        start_date = datetime.now() - timedelta(days=7)
        default_format_str = '%m/%d %Hh'  # '월/일 시'
    else:  # 30일 or 전체 (9999)
        days_to_subtract = 99999 if days >= 9999 else days
        start_date = datetime.now() - timedelta(days=days_to_subtract)
        default_format_str = '%m/%d'  # '월/일'

    # 2. DB에서 데이터 조회
    logs = db.query(IndexLog) \
        .filter(IndexLog.created_at >= start_date) \
        .order_by(IndexLog.created_at) \
        .all()

    # 3. [핵심 수정] X축 포맷 최종 결정
    date_format_str = default_format_str

    if logs and days > 1:  # 데이터가 있고, 24시간 뷰가 아닐 때
        # 첫 데이터와 마지막 데이터의 날짜 차이 계산
        first_date = logs[0].created_at.date()
        last_date = logs[-1].created_at.date()
        date_span_days = (last_date - first_date).days

        # 30일/전체 뷰를 요청했으나, 데이터가 2일치 이하일 경우 (X축 중복 방지)
        if (days > 7 and date_span_days <= 2):
            date_format_str = '%m/%d %H:%M'  # 강제로 '시:분' 포맷 사용

    # 4. 차트 데이터 포맷팅
    categories = []
    performance_data = []
    fandom_data = []
    buzz_data = []

    for log in logs:
        # 최종 결정된 date_format_str을 사용
        categories.append(log.created_at.strftime(date_format_str))
        performance_data.append(log.performance_index)
        fandom_data.append(log.fandom_index)
        buzz_data.append(log.buzz_index)

    return IndexTrendResponse(
        categories=categories,
        performance_data=performance_data,
        fandom_data=fandom_data,
        buzz_data=buzz_data
    )