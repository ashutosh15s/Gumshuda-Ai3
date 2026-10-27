import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth_routes, case_routes, sighting_routes, admin_routes
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gumshuda Core API",
    description="Privacy First Missing Persons Coordination Grid",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Mount media upload access
app.mount("/cases_media", StaticFiles(directory=settings.UPLOAD_DIR), name="cases_media")

# Include API Routers
app.include_router(auth_routes.router)
app.include_router(case_routes.router)
app.include_router(sighting_routes.router)
app.include_router(admin_routes.router)

# Root route: Serves index.html to browser
@app.get("/", response_class=HTMLResponse)
@app.get("/verify", response_class=HTMLResponse)
@app.get("/admin", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Gumshuda Core"}