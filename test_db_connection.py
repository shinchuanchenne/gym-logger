from sqlmodel import Session
from app.db.engine import engine

with Session(engine) as session:
    print("Database connection OK!")