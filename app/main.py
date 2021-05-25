from fastapi import FastAPI

from .views import router as evox_api_router

app = FastAPI()
app.include_router(evox_api_router, tags=["evox"])
