from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import question
from app.database import Base, engine
# Import models to ensure they're registered with Base before table creation
from app.models import question as question_model

# Create tables - models must be imported first
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KCLoft MVP API")

# Configure CORS - must be added before routes
# This allows requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers (including Authorization)
    expose_headers=["*"],
)

# Add exception handlers to ensure CORS headers are included in error responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173"},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    print(f"Unhandled exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173"},
    )

# Test endpoint to verify CORS is working
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

app.include_router(question.router)
