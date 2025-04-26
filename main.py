from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.todos import router as todos_router
from routes.scrape import router as scrape_router
from routes.jobs import router as job_router
from config.database import job_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await job_collection.create_index("more_details", unique=True)
    print("✅ Created unique index on 'more_details' field")

    yield  # App runs here

    # Shutdown logic (optional)
    print("🚪 Shutting down...")

# Pass lifespan to FastAPI constructor
app = FastAPI(lifespan=lifespan)

app.include_router(todos_router)
app.include_router(scrape_router)
app.include_router(job_router)
