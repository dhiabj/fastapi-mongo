from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import client, job_collection
from routes.todos import router as todos_router
from routes.scrape import router as scrape_router
from routes.jobs import router as job_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        await client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Create unique index
    try:
        await job_collection.create_index("more_details", unique=True)
        print("✅ Created unique index on 'more_details' field")
    except Exception as e:
        print(f"❗ Error creating index: {e}")

    yield

    # Shutdown logic (optional)
    print("🚪 Shutting down...")

# Pass lifespan to FastAPI constructor
app = FastAPI(lifespan=lifespan)

app.include_router(todos_router)
app.include_router(scrape_router)
app.include_router(job_router)
