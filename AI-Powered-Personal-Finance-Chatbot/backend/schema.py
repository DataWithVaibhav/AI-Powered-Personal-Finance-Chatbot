from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    data: Optional[List[dict]] = None

class BudgetCreate(BaseModel):
    category: str
    monthly_budget: float

class SpendingAlert(BaseModel):
    category: str
    budget: float
    spent: float
    overspend_amount: float
    overspend_percent: float

class SessionCreate(BaseModel):
    session_name: Optional[str] = "Default Session"

class SessionInfo(BaseModel):
    session_id: str
    session_name: str
    created_at: datetime
    last_activity: datetime
    has_data: bool