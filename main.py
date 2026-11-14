import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Meta Webhook Server")

# Define your secure verify token (must match what you enter in the Meta App Dashboard)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "osareghe5259")

@app.get("/")
async def root():
    return {"status": "online", "service": "Meta Webhook Listener"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Handles Meta's verification handshake (GET request).
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED: Successfully verified webhook token with Meta.")
            # Must return the raw challenge string as plain text with a 200 status code
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Verification token mismatch")
    
    raise HTTPException(status_code=400, detail="Missing parameters")

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Handles incoming real-time updates and events from Facebook and Instagram (POST request).
    """
    try:
        body = await request.json()
        print("Received webhook event:", body)
        
        # TODO: Add your custom logic here to process messages, comments, or media changes
        
        # Always return a 200 OK quickly so Meta knows the event was received
        return {"status": "received"}
    except Exception as e:
        print(f"Error processing webhook event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
