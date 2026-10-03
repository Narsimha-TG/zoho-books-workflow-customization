from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Zoho Books Workflow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuoteRequest(BaseModel):
    quote_id: str
    template_type: str
    client_id: str

class WebhookPayload(BaseModel):
    quote_id: str
    status: str

# In-memory seed data
quotes_db = {
    "Q-1001": {"quote_id": "Q-1001", "status": "Draft", "pdf_url": None}
}

@app.post("/api/v1/quote/generate")
def generate_quote(request: QuoteRequest):
    quotes_db[request.quote_id] = {
        **request.dict(),
        "status": "Generated",
        "pdf_url": f"https://cdn.zoho.com/pdf/{request.quote_id}.pdf",
        "created_at": datetime.utcnow().isoformat()
    }
    return {"message": "PDF generated successfully", "data": quotes_db[request.quote_id]}

@app.post("/api/v1/webhook/zoho-books")
def handle_webhook(payload: WebhookPayload):
    if payload.quote_id in quotes_db:
        quotes_db[payload.quote_id]["status"] = payload.status
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Quote not found")

@app.get("/api/v1/templates/metadata")
def get_metadata():
    return {
        "templates": ["Project", "Maintenance", "Generic"],
        "mapping": {"Project": "P-001", "Maintenance": "M-001", "Generic": "G-001"}
    }