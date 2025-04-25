from fastapi import FastAPI
from routes.todos import router as todos_router
from routes.scrape import router as scrape_router
from routes.jobs import router as job_router

app = FastAPI()

app.include_router(todos_router)
app.include_router(scrape_router)
app.include_router(job_router)
