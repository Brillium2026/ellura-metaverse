import hmac
import hashlib
import os
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, EvolveLog
from ..auth import get_password_hash
from datetime import datetime

router = APIRouter()

LEMONSQUEEZY_WEBHOOK_SECRET = os.getenv("LEMONSQUEEZY_WEBHOOK_SECRET")

@router.post("/lemonsqueezy")
async def lemonsqueezy_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Autonomous Financial Gateway.
    Handles the handshake and provisions the Substrate.
    """
    signature = request.headers.get("X-Signature")
    payload = await request.body()
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    digest = hmac.new(
        LEMONSQUEEZY_WEBHOOK_SECRET.encode(), 
        payload, 
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, digest):
        raise HTTPException(status_code=400, detail="Invalid signature - Handshake failed")

    data = await request.json()
    event_name = data.get("meta", {}).get("event_name")
    attributes = data.get("data", {}).get("attributes", {})
    email = attributes.get("user_email")

    if event_name in ["subscription_created", "order_created"]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            temp_password = get_password_hash(os.urandom(12).hex())
            user = User(
                email=email, 
                hashed_password=temp_password,
                is_active=True
            )
            db.add(user)
            db.flush()
            
            log = EvolveLog(
                message=f"Substrate Provisioned: Marketplace activation via {event_name}",
                user_id=user.id
            )
            db.add(log)
            
        db.commit()
        return {"status": "success", "message": "Substrate activated"}

    if event_name == "subscription_cancelled":
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_active = False
            db.commit()
        return {"status": "success", "message": "Substrate deactivated"}

    return {"status": "ignored", "message": "Event not handled"}
