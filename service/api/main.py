from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from service.api import services, schema
from service.core.database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Roro Index API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "Roro API"}


@app.get("/api/v1/index/snapshot", response_model=schema.IndexSnapshotResponse)
def get_current_snapshot(db: Session = Depends(get_db)):
    return services.get_snapshot_data(db=db)


@app.get("/api/v1/index/trend", response_model=schema.IndexTrendResponse)
def get_index_trends(days: int = 30, db: Session = Depends(get_db)):
    return services.get_trend_data(db=db, days=days)