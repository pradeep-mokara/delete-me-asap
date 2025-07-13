from fastapi import FastAPI
from .api import router

app = FastAPI(title="QualGent Job Server")

app.include_router(router)
