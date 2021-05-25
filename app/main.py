from fastapi import FastAPI
from .views import router as evox_api_router

app = FastAPI(
    title="EvoxAPI",
    description="Daftcode recruitment task.",
)
app.include_router(evox_api_router, tags=["evox"])
