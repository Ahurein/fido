from fastapi import FastAPI
from src.core.config import config
from src.core.lifespan_event import lifespan

app = FastAPI(
    title="Fido API",
    description="Api for user transactions",
    version=config.VERSION,
    lifespan=lifespan
)