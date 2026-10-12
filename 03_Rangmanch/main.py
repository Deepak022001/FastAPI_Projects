from contextlib import asynccontextmanager
from email import message

from fastapi import FastAPI

from database import create_tables
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    # Shut down:Cleanup  here
    print("Shutting down the app ")


app = FastAPI(
    title="Rangmanch Reviews API",
    description="Theatre reviews api for pune rangmanch",
    lifespan=lifespan,
)

app.include_router(reviews_router)


@app.get("/")
def root():
    return {message: "Welcome to rangmanch review API"}
