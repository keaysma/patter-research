from typing import Optional, List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import controller, types, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://pattern.test"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/fills/{fill_timestamp}', response_model=Optional[types.Fill])
def get_fill_api(fill_timestamp: str, db: Session = Depends(get_db)):
    return controller.get_fill(db, fill_timestamp)

@app.get('/fills', response_model=types.FillList)
def get_fills_in_range_api(
    db: Session = Depends(get_db), 
    start: int = 0, 
    end: int = 0, 
    symbol: Optional[str] = None, 
    exchange: Optional[str] = None,
    groupBy: Optional[str] = None
):
    fills = controller.get_fills_in_range(db, start, end, symbol, exchange)
    return {
        "fills": fills,
        "count": len(fills)
    }