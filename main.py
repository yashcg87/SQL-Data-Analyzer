from fastapi import FastAPI
from app.jobs.kb_update import lifespan
from app.routes.chat import router


app = FastAPI()

app.include_router(router)