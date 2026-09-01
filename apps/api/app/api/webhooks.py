from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
from app.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/razorpay")
async def razorpay_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
        
    # Verify signature
    secret = settings.RAZORPAY_WEBHOOK_SECRET
    if secret:
        expected_sig = hmac.new(
            bytes(secret, 'latin-1'),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_sig, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")
            
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
    event = data.get("event")
    logger.info(f"Received Razorpay Webhook Event: {event}")
    
    # Normally we would trigger a Temporal workflow here based on the event
    if event == "payment.captured":
        # Handle payment capture
        pass
    elif event == "transfer.processed":
        # Handle Route transfer
        pass
    elif event == "settlement.processed":
        # Handle settlement
        pass
        
    return {"status": "ok"}
