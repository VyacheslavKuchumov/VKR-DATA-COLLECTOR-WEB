from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.websocket.websocketEndpoint import router as websocket_router
from app.routers.student_router import router as student_router
from app.routers.region_router import router as region_router
from app.routers.hh_ru_credentials_router import router as hh_ru_credentials_router



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
app.include_router(student_router, prefix="/students", tags=["students"])
app.include_router(region_router, prefix="/regions", tags=["regions"])
app.include_router(hh_ru_credentials_router, prefix="/hh-ru-credentials", tags=["hh_ru_credentials"])


# websockets
app.include_router(websocket_router)
