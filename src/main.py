from fastapi import FastAPI
from src.core.config import config
from src.core.lifespan_event import lifespan

from src.routes_handlers.transactions_router import transactions_router

app = FastAPI(
    title="Fido API",
    description="Api for user transactions",
    version=config.VERSION,
    lifespan=lifespan
)

app.include_router(transactions_router, prefix=f"/api/{config.VERSION}/transactions", tags=["Transactions"])

