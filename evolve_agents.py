import math
from datetime import datetime

class EvolveOne:
    def __init__(self, db_session):
        self.db = db_session
        self.STABILITY_THRESHOLD = 90.0
        self.LAMBDA = 0.05  # Decay rate; reset by last_interaction_at

    def get_stability_metrics(self, assessment):
        """Calculates the 'Density' of the field"""
        last_act = assessment.last_interaction_at or assessment.created_at
        days_since = (datetime.utcnow() - last_act).total_seconds() / 86400.0
        
        # Exponential decay calculation
        coherence = math.exp(-self.LAMBDA * days_since)
        stability_score = assessment.performance_score * coherence
        
        status = "STABLE"
        if coherence < 0.8:
            status = "COHERENCE DECAYING"
        if assessment.performance_score >= self.STABILITY_THRESHOLD:
            status = "HARDENING MODE" if coherence >= 0.9 else "STABILITY CRITICAL"
            
        return {
            "score": round(stability_score, 1),
            "coherence": round(coherence, 2),
            "status": status
        }

    def weekly_evaluation(self):
        """Autonomous cycle: Hardening vs Expansion"""
        from .models import Assessment, EvolveLog
        assessments = self.db.query(Assessment).all()
        
        for ass in assessments:
            last_activity = ass.last_interaction_at or ass.created_at
            days_since = (datetime.utcnow() - last_activity).days
            
            # Physics Check: Are we at high amplitude (90%+)?
            if ass.performance_score >= self.STABILITY_THRESHOLD:
                # HARDENING: Focus on consistency/density
                improvement = (5.0 * math.exp(-self.LAMBDA * days_since)) * 0.6
                msg = f"EVOLVE-1: Hardened {ass.title} structure (+{improvement:.1f}%)"
            else:
                # EXPANSION: Focus on growth
                improvement = 12.0 * math.exp(-self.LAMBDA * days_since)
                msg = f"EVOLVE-1: Expanded {ass.title} opportunities (+{improvement:.1f}%)"

            ass.performance_score = min(100.0, ass.performance_score + improvement)
            ass.last_evolved_at = datetime.utcnow()
            
            self.db.add(EvolveLog(message=msg, user_id=ass.owner_id))
        
        self.db.commit()
