from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.db import DbConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DbConfig.init_db()
    yield