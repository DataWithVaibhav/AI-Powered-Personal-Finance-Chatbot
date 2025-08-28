from sqlalchemy import Column, Integer, String, Date, Float, Boolean, DateTime
from datetime import datetime
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    description = Column(String, nullable=False)
    merchant = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    monthly_budget = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    session_name = Column(String, default="Default Session")
    transactions_data = Column(String)  # JSON string of transactions
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)