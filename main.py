from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, engine
 import models, auth
from .evolve_agents import EvolveOne

# Initialize the Substrate
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BrilliantMetaverse 2026")

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
