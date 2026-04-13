import threading
import time
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.job_routes import router as job_router
from app.routes.auth_routes import router as auth_router
from app.models.user import create_users_table
from app.models.job import create_jobs_table
from app.scheduler.fetch_jobs import run_scraper

app = FastAPI(title="Reddit Job Board API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def scraper_loop():
    """Background loop to run the scraper every 4 hours."""
    while True:
        try:
            run_scraper()
        except Exception as e:
            print(f"[CRITICAL] Scraper loop failed: {e}")
        
        # 4 hours = 4 * 3600 seconds
        time.sleep(4 * 3600)

# Include routers
app.include_router(auth_router)
app.include_router(job_router)

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Auto-create tables on startup
@app.on_event("startup")
def startup():
    # Create tables
    create_users_table()
    create_jobs_table()
    
    # Start the background scraper thread
    thread = threading.Thread(target=scraper_loop, daemon=True)
    thread.start()
    print("[INIT] Background scraper thread started (4-hour cycle)")

@app.get("/")
def home():
    """Redirect to the frontend login page."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")