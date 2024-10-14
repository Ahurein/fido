from fastapi import FastAPI
from src.core.config import config
from src.core.lifespan_event import lifespan
from src.middlewares.exception_middlewares import add_exception_middleware
from src.routes_handlers.analytics_router import analytics_router
from fastapi.middleware.cors import CORSMiddleware

from src.routes_handlers.transactions_router import transactions_router
from src.schemas.api_response import success_response

app = FastAPI(
    title="Fido API",
    description="Api for user transactions",
    version=config.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_middleware(app)

@app.get("/", tags=["Health"])
async def healthcheck():
    return success_response(message="Backend is running")

app.include_router(transactions_router, prefix=f"/api/{config.VERSION}/transactions", tags=["Transactions"])
app.include_router(analytics_router, prefix=f"/api/{config.VERSION}/analytics", tags=["Analytics"] )