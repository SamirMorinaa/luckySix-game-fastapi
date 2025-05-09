from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.routers.runda import izvuci_brojeve
from app.database import engine
from app.models import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize APScheduler
scheduler = BackgroundScheduler()

# Add a job that runs every 5 hours
scheduler.add_job(izvuci_brojeve, "interval", hours=5)
scheduler.start()

# Add a shutdown event for the scheduler
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

# Include routes from your modules
from app.routers import game, listici, boje, saldo
app.include_router(game.router)
app.include_router(listici.router)
app.include_router(boje.router)
app.include_router(saldo.router)
# app.include_router(runda.router)  # Uncomment if needed
