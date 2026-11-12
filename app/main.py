from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import messages_router, jobs_router, health_router
from app.utilities.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="WhatsApp Scheduler API",
    description="Schedule and send WhatsApp messages via Twilio.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(messages_router)
app.include_router(jobs_router)
app.include_router(health_router)
