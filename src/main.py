from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router

# Initialize the FastAPI app with metadata
app = FastAPI(
    title="Feature File Generator API",
    description="A service to generate Gherkin .feature files using a configurable LLM.",
    version="0.1.0",
)

# Add CORS middleware to allow requests from your React frontend
# In a production environment, you would restrict origins to your frontend's domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/", summary="Check API status", tags=["Health Check"])
def read_root():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "message": "API is running"}