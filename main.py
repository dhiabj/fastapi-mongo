from fastapi import FastAPI
from routes.todos import router

app = FastAPI()

app.include_router(router)
