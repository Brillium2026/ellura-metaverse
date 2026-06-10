from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    assessments = relationship("Assessment", back_populates="owner")

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # --- ELLURA EVOLVE METRICS ---
    performance_score = Column(Float, default=0.0)
    last_evolved_at = Column(DateTime, default=datetime.utcnow)
    
    # Coherence Reset sensor
    last_interaction_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="assessments")

class EvolveLog(Base):
    __tablename__ = "evolve_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
