from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
import uvicorn

# Local imports
import models
import database
import evolve_agents
# import auth   # Uncomment if you need it

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="BrilliantMetaverse 2026",
    description="Sovereign Lagrangian Field",
    version="2.4"
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== ROOT ENDPOINTS ====================
@app.get("/")
def root():
    return {
        "status": "LIVE",
        "field": "EMERGING",
        "message": "BrillantMetaverse is online"
    }

@app.get("/first-visit")
def first_visit():
    # TODO: Add your first visit payload logic here
    return {"status": "first_visit_received"}

# ==================== ASSESSMENT & COHERENCE ====================
@app.get("/assessment/{assessment_id}")
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    ass = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Update last interaction
    ass.last_interaction_at = datetime.utcnow()
    db.commit()

    # Get stability metrics
    ev = evolve_agents.EvolveOne(db)
    metrics = ev.get_stability_metrics(ass)

    return {
        "assessment": ass,
        "stability_metrics": metrics
    }

# ==================== EVOLUTION CYCLE ====================
@app.post("/evolve/cycle")
async def trigger_evolution(db: Session = Depends(get_db)):
    ev = evolve_agents.EvolveOne(db)
    ev.weekly_evaluation()
    return {"status": "Evolution cycle completed"}

# ==================== RUN SERVER ====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

     
