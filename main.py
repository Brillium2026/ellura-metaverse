from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
import database
import evolve_agents
import models
import auth
# Initialize the Substrate
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BrilliantMetaverse 2026")
agent = evolve_agents.EvolveOne()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/assessment/{assessment_id}")
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """
    This endpoint acts as the COHERENCE RESET.
    Every time Brilliance fetches the data, the sensor updates.
    """
    ass = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Substrate entry not found")
    
    # REFRESH THE SENSOR
    ass.last_interaction_at = datetime.utcnow()
    db.commit()
    
    # Get the visual density metrics for the dashboard
    ev = EvolveOne(db)
    metrics = ev.get_stability_metrics(ass)
    
    return {
        "assessment": ass,
        "stability_metrics": metrics
    }

@app.post("/evolve/cycle")
async def trigger_evolution(db: Session = Depends(get_db)):
    """
    Manual trigger for the EVOLVE-1 cycle.
    In production, this is called weekly by the Render background worker.
    """
    ev = EvolveOne(db)
    ev.weekly_evaluation()
    return {"status": "Evolution cycle complete. Stability hardening applied."}
import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

# Local project imports
import models
import auth
from database import engine, SessionLocal, get_db  # Assuming get_db is moved to database.py
from evolve_agents import EvolveOne
from .engine import build_first_visit_payload

# Initialize Database Substrate
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BrilliantMetaverse 2026")

# 1. Root & Discovery Endpoints
@app.get("/")
def root():
    return {
        "status": "LIVE",
        "field": "EMERGING",
        "app": "BrilliantMetaverse"
    }

@app.get("/first-visit")
def first_visit():
     build_first_visit_payload()

# 2. Coherence & Assessment Logic
@app.get("/assessment/{assessment_id}")
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """
    COHERENCE RESET: Updates the sensor every time data is fetched.
    """
    ass = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Substrate entry not found")

    # REFRESH THE SENSOR
    ass.last_interaction_at = datetime.utcnow()
    db.commit()

    # Calculate visual density/stability
    ev = EvolveOne(db)
    metrics = ev.get_stability_metrics(ass)
    
    return {
        "assessment": ass,
        "stability_metrics": metrics
    }

# 3. Evolutionary Cycles
@app.post("/evolve/cycle")
async def trigger_evolution(db: Session = Depends(get_db)):
    """
    Manual trigger for EVOLVE-1. 
    Usually managed by background workers on Render/Heroku.
    """
    ev = EvolveOne(db)
    ev.weekly_evaluation()
    return {"status": "Evolution cycle complete. Stability hardening applied."}

# 4. Execution Logic
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


     
