from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

