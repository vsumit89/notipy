from fastapi import FastAPI
from utils.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
import time
from api.routes.v1.event_manager import events_manager_router


settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.PROJECT_DOCS_URL,
)

# adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# adding middleware to add process time header which helps in debugging / profiling
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(events_manager_router, tags=["events"])
