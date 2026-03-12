from fastapi import FastAPI
from app.routers import api_router

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "GymLogger API is running."}

app.include_router(api_router)