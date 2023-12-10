# importing external modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# importing inbuilt modules
import time

# importing custom modules
from api.routes.v1.event_manager import events_manager_router
from api.routes.v1.register_service import registration_router

from api.middleware.validate_service_token import token_middleware

from utils.config import get_settings
from utils.logger import CustomLogger
from app.repositories.db_factory import getDB

settings = get_settings()

logger = CustomLogger(__name__)

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


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up")
    try:
        # setting up the database connection
        db_service = getDB(settings.DB_STORE)
        await db_service.connect()
    except Exception as e:
        logger.error(f"Error starting up: {e}")


# adding middleware to add process time header which helps in debugging / profiling
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def validate_service_token(request, call_next):
    if request.url.path == "/register":
        return await call_next(request)

    try:
        response = await token_middleware(request=request, call_next=call_next)
        return response
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail},
        )


app.include_router(events_manager_router, tags=["events"], prefix="/api/v1")
app.include_router(registration_router, tags=["registration"], prefix="/api/v1")
