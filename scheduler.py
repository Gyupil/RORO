import time
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session
from service.core.database import SessionLocal, engine, Base
from service.core.models import IndexLog
from service.core.calculate_roro import calculate_total_index
import random


def run_calculation_job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 스케줄러 작업 시작: 지수 계산 중...")
    db: Session = SessionLocal()

    try:
        results = calculate_total_index()

        perf = results.get('details', {}).get('indices', {}).get('performance_index', 0)
        fand = results.get('details', {}).get('indices', {}).get('fandom_index', 0)
        buzz = results.get('details', {}).get('indices', {}).get('buzz_index', 0)

        JITTER_RATIO = 0.01
        W_PERF = 0.40
        W_FANDOM = 0.35
        W_BUZZ = 0.25

        perf_noise = (random.random() - 0.35) * 2 * (perf * JITTER_RATIO)
        fand_noise = (random.random() - 0.35) * 2 * (fand * JITTER_RATIO)
        buzz_noise = (random.random() - 0.35) * 2 * (buzz * JITTER_RATIO)

        jittered_perf = perf + perf_noise
        jittered_fand = fand + fand_noise
        jittered_buzz = buzz + buzz_noise
        jittered_total = (jittered_perf * W_PERF) + (jittered_fand * W_FANDOM) + (jittered_buzz * W_BUZZ)

        new_log = IndexLog(
            total_index=jittered_total,
            performance_index=jittered_perf,
            fandom_index=jittered_fand,
            buzz_index=jittered_buzz
        )

        db.add(new_log)
        db.commit()

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 작업 완료: DB 저장 성공 (Total: {jittered_total})")

    except Exception as e:
        print(f"!!! 스케줄러 작업 실패: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    scheduler = BlockingScheduler(timezone='Asia/Seoul')
    scheduler.add_job(run_calculation_job, 'interval', hours=0.2, jitter=120)

    run_calculation_job()

    print("스케줄러 시작... (12분마다 지수 계산 실행)")
    scheduler.start()