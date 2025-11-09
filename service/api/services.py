from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from service.core.models import IndexLog
from service.api.schema import IndexSnapshotResponse, IndexTrendResponse
from datetime import datetime, timedelta


def get_snapshot_data(db: Session) -> IndexSnapshotResponse:
    latest_log = db.query(IndexLog).order_by(desc(IndexLog.created_at)).first()

    if not latest_log:
        return IndexSnapshotResponse(
            total_index=0, total_index_change_24h=0,
            performance_index=0, performance_index_change_24h=0,
            fandom_index=0, fandom_index_change_24h=0,
            buzz_index=0, buzz_index_change_24h=0
        )

    time_24h_ago = latest_log.created_at - timedelta(days=1)
    prev_log = db.query(IndexLog) \
        .filter(IndexLog.created_at <= time_24h_ago) \
        .order_by(desc(IndexLog.created_at)) \
        .first()

    total_change = 0
    perf_change = 0
    fand_change = 0
    buzz_change = 0

    if prev_log:
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
    if days == 1:
        start_date = datetime.now() - timedelta(days=1)
        default_format_str = '%H:%M'
    elif days <= 7:
        start_date = datetime.now() - timedelta(days=7)
        default_format_str = '%m/%d %Hh'
    else:
        days_to_subtract = 99999 if days >= 9999 else days
        start_date = datetime.now() - timedelta(days=days_to_subtract)
        default_format_str = '%m/%d'

    logs = db.query(IndexLog) \
        .filter(IndexLog.created_at >= start_date) \
        .order_by(IndexLog.created_at) \
        .all()

    date_format_str = default_format_str

    if logs and days > 1:
        first_date = logs[0].created_at.date()
        last_date = logs[-1].created_at.date()
        date_span_days = (last_date - first_date).days

        if (days > 7 and date_span_days <= 2):
            date_format_str = '%m/%d %H:%M'

    categories = []
    performance_data = []
    fandom_data = []
    buzz_data = []

    for log in logs:
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