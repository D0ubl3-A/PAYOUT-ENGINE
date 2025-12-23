from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import health, payouts
from routers import ingest_screenshot, extractions, audits, invoices
from settings import settings

app = FastAPI(title="Payout API")

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(payouts.router, prefix="/payouts", tags=["payouts"])
app.include_router(ingest_screenshot.router, tags=["uploads"])
app.include_router(extractions.router, tags=["extractions"])
app.include_router(audits.router, tags=["audits"])
app.include_router(invoices.router, tags=["invoices"])
