from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.websocket.websocketEndpoint import router as websocket_router
from app.routers.student_router import router as student_router
from app.routers.region_router import router as region_router
from app.routers.hh_ru_credentials_router import router as hh_ru_credentials_router
from app.routers.job_router import router as job_router

from app.routers.user_router import router as user_router
from app.routers.data_source_router import router as data_source_router
from app.routers.minstat_worker_router import router as minstat_worker_router
from app.routers.hh_ru_dataset_router import router as hh_ru_dataset_router

app = FastAPI(root_path="/api",
    title="Data collector API",
    description="Sluvik's API"
)

# Define allowed origins (adjust the list to your requirements)
origins = [
    "https://data.vyachik-dev.ru",
    "http://localhost:8080",
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],    # Allows all headers
)


# Include routers
app.include_router(minstat_worker_router, prefix="/minstat-workers", tags=["minstat_workers"])
app.include_router(hh_ru_dataset_router, prefix="/hh-ru-dataset", tags=["hh_ru_datasets"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(data_source_router, prefix="/data-sources", tags=["data_sources"])

app.include_router(region_router, prefix="/regions", tags=["regions"])
app.include_router(hh_ru_credentials_router, prefix="/hh-ru-credentials", tags=["hh_ru_credentials"])
app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(student_router, prefix="/students", tags=["students"])



# websockets
app.include_router(websocket_router)
