import re
import json
import uuid
import io
import time
from datetime import date, datetime, timedelta
from typing import Tuple, Optional, List, Dict
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, text, case
from sqlalchemy.orm import Session
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Absolute imports
from backend.db import Base, engine, get_db
from backend.models import Transaction, Budget, UserSession
from backend.schema import ChatRequest, ChatResponse

# -------------------------
# CATEGORY ALIASES & AI MODEL
# -------------------------
CATEGORY_ALIASES = {
    "food": ["food", "dining", "groceries", "restaurant", "cafe", "meal", "grocery", "snacks", "dinner", "lunch", "breakfast", "ccd"],
    "transport": ["transport", "transportation", "uber", "ola", "cab", "taxi", "fuel", "bus", "train", "metro", "petrol", "ride"],
    "shopping": ["shopping", "amazon", "flipkart", "myntra", "mall", "store", "clothing", "electronics", "purchase", "online"],
    "bills": ["bills", "utilities", "electricity", "wifi", "phone", "internet", "rent", "water", "mobile", "recharge", "bill", "gas"],
    "health": ["health", "doctor", "hospital", "pharmacy", "medicine", "healthcare", "gym", "dental"],
    "entertainment": ["entertainment", "movies", "cinema", "netflix", "game", "concert", "pvr", "ticket", "subscription", "movie", "bowling"],
    "education": ["education", "school", "college", "tuition", "course", "udemy", "book", "certification"],
    "investment": ["investment", "stocks", "mutual fund", "dividend", "sip"],
    "income": ["salary", "income", "freelance", "bonus", "deposit", "payment"]
}

# Load or create AI model for categorization
def load_ai_model():
    model_path = "ai_category_model.pkl"
    vectorizer_path = "ai_vectorizer.pkl"
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        return joblib.load(model_path), joblib.load(vectorizer_path)
    else:
        return None, None

ai_model, ai_vectorizer = load_ai_model()

# Global timestamp to force frontend refresh
data_timestamp = time.time()

# -------------------------
# UTILS
# -------------------------
def normalize_category(text: str) -> str:
    if not text:
        return "Uncategorized"
    t = text.strip().lower()
    for k, vals in CATEGORY_ALIASES.items():
        if t == k or any(v in t for v in vals):
            return k.capitalize()
    return t.capitalize()

def extract_merchant(description: str) -> str:
    if not description:
        return "Unknown"
    m = re.sub(r"[^A-Za-z0-9\s]", "", description).strip()
    if not m:
        return "Unknown"
    return " ".join(m.split()[:2]).title()

def parse_csv_date(date_str: str) -> date:
    date_str = date_str.strip().replace("/", "-")
    formats_to_try = [
        '%d-%m-%Y', '%Y-%m-%d', '%m-%d-%Y', '%d-%m-%y'
    ]
    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    print(f"Warning: Unable to parse date '{date_str}'. Using today's date.")
    return date.today()

def parse_time_window(q: str, db: Session = None) -> Tuple[Optional[date], Optional[date]]:
    ql = q.lower()
    if db is not None:
        latest_date = db.query(func.max(Transaction.date)).scalar()
        if latest_date:
            today = latest_date
        else:
            today = date.today()
    else:
        today = date.today()

    if "last month" in ql:
        if today.month == 1:
            last_month = 12
            year = today.year - 1
        else:
            last_month = today.month - 1
            year = today.year
        start = date(year, last_month, 1)
        if last_month == 12:
            end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(year, last_month + 1, 1) - timedelta(days=1)
        return start, end

    if "this month" in ql:
        start = today.replace(day=1)
        if start.month == 12:
            end = date(start.year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(start.year, start.month + 1, 1) - timedelta(days=1)
        return start, end

    if "this week" in ql:
        start = today - timedelta(days=today.weekday())
        return start, start + timedelta(days=6)

    if "last week" in ql:
        start = today - timedelta(days=today.weekday() + 7)
        return start, start + timedelta(days=6)

    return None, None

def extract_category(q: str) -> Optional[str]:
    ql = q.lower()
    for k, vals in CATEGORY_ALIASES.items():
        if k in ql or any(v in ql for v in vals):
            return k.capitalize()
    if any(word in ql for word in ["food", "restaurant", "grocery", "dinner", "lunch", "snack"]):
        return "Food"
    if any(word in ql for word in ["movie", "netflix", "concert", "entertain"]):
        return "Entertainment"
    if any(word in ql for word in ["shopping", "amazon", "mall", "store"]):
        return "Shopping"
    if any(word in ql for word in ["transport", "petrol", "metro", "uber"]):
        return "Transport"
    if any(word in ql for word in ["bill", "electricity", "water", "mobile"]):
        return "Bills"
    return None

def parse_topn(q: str, default: int = 3) -> int:
    m = re.search(r"(top|biggest|highest)\s*(\d+)", q.lower())
    return int(m.group(2)) if m else default

def classify_intent(q: str) -> str:
    ql = q.lower()
    if any(word in ql for word in ["how much", "spent", "spend", "expense", "total", "amount"]) and extract_category(ql):
        return "sum_by_category"
    if "growing" in ql or "trend" in ql or "increase" in ql:
        return "fastest_growing_category"
    if any(word in ql for word in ["biggest", "top", "highest", "largest"]) and any(word in ql for word in ["expense", "spend", "purchase"]):
        return "top_expenses"
    if any(word in ql for word in ["list", "show", "what are", "which"]):
        return "list_transactions"
    if any(word in ql for word in ["alert", "overspend", "budget", "limit"]):
        return "spending_alerts"
    return "fallback"

def train_ai_categorization_model(db: Session):
    """Train AI model on existing categorized transactions"""
    transactions = db.query(Transaction).filter(Transaction.category != "Uncategorized").all()
    
    if len(transactions) < 10:
        return None, None
    
    descriptions = [f"{t.description} {t.merchant}" for t in transactions]
    categories = [t.category for t in transactions]
    
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(descriptions)
    
    model = MultinomialNB()
    model.fit(X, categories)
    
    joblib.dump(model, "ai_category_model.pkl")
    joblib.dump(vectorizer, "ai_vectorizer.pkl")
    
    return model, vectorizer

def ai_categorize_transaction(description: str, merchant: str):
    """Use AI to categorize uncategorized transactions"""
    global ai_model, ai_vectorizer
    
    if ai_model is None or ai_vectorizer is None:
        return "Uncategorized"
    
    text_input = f"{description} {merchant}"
    X = ai_vectorizer.transform([text_input])
    prediction = ai_model.predict(X)
    
    return prediction[0]

def format_currency(amount: float) -> str:
    """Format amount as currency with proper sign"""
    if amount >= 0:
        return f"₹{amount:,.2f}"
    else:
        return f"-₹{abs(amount):,.2f}"

# -------------------------
# APP SETUP
# -------------------------
app = FastAPI(title="AI Finance Chatbot")

# 🚫 Disable caching globally
@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# -------------------------
# ROUTES
# -------------------------
@app.get("/")
def root():
    return {"message": "🚀 AI Finance Chatbot Backend is running! Use /docs to explore the API."}

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    global data_timestamp
    try:
        if not file.filename or not file.filename.endswith(".csv"):
            return {"ok": False, "error": "Please upload a CSV file."}

        # Read file content
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # DEBUG: Print what we received
        print(f"CSV columns: {df.columns.tolist()}")
        print(f"First 5 rows:\n{df.head()}")
        
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]
        print(f"Normalized columns: {df.columns.tolist()}")
        
        # Check for required columns
        expected = {"date", "description", "amount", "category"}
        if not expected.issubset(set(df.columns)):
            return {"ok": False, "error": f"CSV must have columns: {expected}. Found: {df.columns.tolist()}"}

        # Process dates
        print("Processing dates...")
        df['date'] = df['date'].apply(parse_csv_date)
        print(f"Date sample: {df['date'].head()}")
        
        # Process categories
        print("Processing categories...")
        df['category'] = df['category'].fillna("Uncategorized").apply(normalize_category)
        print(f"Category sample: {df['category'].head()}")
        print(f"Unique categories: {df['category'].unique()}")
        
        # Process merchants
        df['merchant'] = df['description'].fillna("").apply(extract_merchant)
        print(f"Merchant sample: {df['merchant'].head()}")
        
        # Process amounts
        df['amount'] = pd.to_numeric(df['amount'], errors="coerce")
        df = df.dropna(subset=["amount", "date"])
        print(f"Amount sample: {df['amount'].head()}")
        print(f"Amount stats - Min: {df['amount'].min()}, Max: {df['amount'].max()}, Mean: {df['amount'].mean()}")

        # AI Categorization for uncategorized transactions
        uncategorized_mask = df['category'] == 'Uncategorized'
        print(f"Uncategorized transactions: {uncategorized_mask.sum()}")
        
        if uncategorized_mask.any():
            global ai_model, ai_vectorizer
            if ai_model is None:
                ai_model, ai_vectorizer = train_ai_categorization_model(db)
            
            if ai_model is not None:
                for idx, row in df[uncategorized_mask].iterrows():
                    predicted_category = ai_categorize_transaction(row['description'], row['merchant'])
                    df.at[idx, 'category'] = predicted_category

        records = [
            Transaction(
                date=row.date,
                description=row.description,
                merchant=row.merchant,
                amount=float(row.amount),
                category=row.category,
            )
            for row in df.itertuples(index=False)
        ]

        # Delete ALL transactions to ensure fresh data
        deleted_count = db.query(Transaction).delete()
        print(f"Deleted {deleted_count} old transactions")
        
        db.add_all(records)
        db.commit()
        
        print(f"Inserted {len(records)} new transactions")
        
        # Verify insertion
        new_count = db.query(Transaction).count()
        print(f"Total transactions in DB after upload: {new_count}")
        
        # Update timestamp to force frontend refresh
        data_timestamp = time.time()

        return {"ok": True, "rows": len(records), "timestamp": data_timestamp}
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return {"ok": False, "error": f"Upload failed: {str(e)}"}

# Summary Endpoints with Date Filtering
@app.get("/summary/by_category")
def by_category(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    # Query for expenses (filter for negative amounts which represent expenses)
    query = db.query(Transaction.category, func.sum(Transaction.amount)).filter(Transaction.amount < 0)
    
    if start_date and end_date:
        start = parse_csv_date(start_date)
        end = parse_csv_date(end_date)
        query = query.filter(Transaction.date.between(start, end))
    
    q = query.group_by(Transaction.category).all()
    
    # Format the data and ensure values are positive for spending visualization
    result = []
    for category, amount in q:
        # For a spending chart, we want the absolute value of expenses
        value = abs(amount)  # Convert expense to positive number
        result.append({"label": category, "value": float(value)})
    
    # Sort by value descending to see largest expenses first
    result.sort(key=lambda x: x['value'], reverse=True)
    return {"data": result, "timestamp": data_timestamp}

@app.get("/summary/top_merchants")
def top_merchants(limit: int = 5, start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Transaction.merchant, func.sum(Transaction.amount).label("total")).filter(Transaction.amount < 0)
    
    if start_date and end_date:
        start = parse_csv_date(start_date)
        end = parse_csv_date(end_date)
        query = query.filter(Transaction.date.between(start, end))
    
    q = query.group_by(Transaction.merchant).order_by(text("total ASC")).limit(limit).all()
    return {"data": [{"label": m, "value": float(abs(v))} for m, v in q], "timestamp": data_timestamp}

@app.get("/summary/monthly_totals")
def monthly_total_expenses(db: Session = Depends(get_db)):
    q = (
        db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.sum(Transaction.amount).label("total")
        )
        .filter(Transaction.amount < 0)
        .group_by('month')
        .order_by('month')
        .all()
    )
    return {"data": [{"label": m, "value": float(abs(v))} for m, v in q], "timestamp": data_timestamp}

# Visualization Endpoints for Charts
@app.get("/visualization/category_pie")
def category_pie_chart_data(db: Session = Depends(get_db)):
    """Data for category pie chart - SHOWS ONLY EXPENSES"""
    # Get only expense categories (amount < 0)
    expense_data = (
        db.query(Transaction.category, func.sum(Transaction.amount).label('total'))
        .filter(Transaction.amount < 0)
        .group_by(Transaction.category)
        .all()
    )
    
    return {
        "labels": [item[0] for item in expense_data],
        "values": [abs(float(item[1])) for item in expense_data],
        "colors": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#FF6384", "#C9CBCF"],
        "timestamp": data_timestamp
    }

@app.get("/visualization/monthly_trend")
def monthly_trend_data(db: Session = Depends(get_db)):
    """Data for monthly trend line chart"""
    monthly_data = (
        db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.sum(case((Transaction.amount < 0, Transaction.amount), else_=0)).label('expenses'),
            func.sum(case((Transaction.amount > 0, Transaction.amount), else_=0)).label('income')
        )
        .group_by('month')
        .order_by('month')
        .all()
    )
    
    return {
        "months": [item[0] for item in monthly_data],
        "expenses": [abs(float(item[1])) for item in monthly_data],
        "income": [float(item[2]) for item in monthly_data],
        "timestamp": data_timestamp
    }

# --- NEW MERCHANT ENDPOINTS ---

@app.get("/visualization/top_merchants_by_total_spending")
def top_merchants_by_total_spending(limit: int = 10, db: Session = Depends(get_db)):
    """
    NEW: Data for top merchants bar chart based on TOTAL combined spending.
    This aggregates all payments to a single merchant.
    """
    data = (
        db.query(Transaction.merchant, func.sum(Transaction.amount).label('total'))
        .filter(Transaction.amount < 0)
        .group_by(Transaction.merchant)
        .order_by(text("total ASC"))  # ASC on negative numbers correctly gets the largest spenders
        .limit(limit)
        .all()
    )
    return {
        "labels": [item[0] for item in data],
        "amounts": [abs(float(item[1])) for item in data],
        "timestamp": data_timestamp
    }

@app.get("/visualization/top_merchants_by_single_payment")
def top_merchants_by_single_payment(limit: int = 10, db: Session = Depends(get_db)):
    """
    NEW: Data for largest SINGLE payments to merchants.
    This shows the biggest individual transactions, without aggregation.
    """
    data = (
        db.query(Transaction.merchant, Transaction.amount, Transaction.date)
        .filter(Transaction.amount < 0)
        .order_by(Transaction.amount.asc())  # .asc() gets the most negative (largest) individual payments
        .limit(limit)
        .all()
    )
    
    # Create descriptive labels like "Amazon (27-Aug)" to differentiate transactions
    return {
        "labels": [f"{item[0]} ({item[2].strftime('%d-%b')})" for item in data],
        "amounts": [abs(float(item[1])) for item in data],
        "timestamp": data_timestamp
    }

# --- END OF NEW ENDPOINTS ---


@app.get("/visualization/income_vs_expenses")
def income_vs_expenses_data(db: Session = Depends(get_db)):
    """Data for income vs expenses overview"""
    # Calculate total income (positive amounts)
    total_income_result = db.query(func.sum(Transaction.amount)).filter(Transaction.amount > 0).scalar()
    total_income = float(total_income_result) if total_income_result else 0.0
    
    # Calculate total expenses (absolute value of negative amounts)
    total_expenses_result = db.query(func.sum(Transaction.amount)).filter(Transaction.amount < 0).scalar()
    total_expenses = abs(float(total_expenses_result)) if total_expenses_result else 0.0
    
    # Calculate net savings
    net_savings = total_income - total_expenses
    
    return {
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "netSavings": net_savings,
        "timestamp": data_timestamp
    }

# Budget Management
@app.post("/budgets")
def set_budget(category: str, monthly_budget: float, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.category == category).first()
    if budget:
        budget.monthly_budget = monthly_budget
    else:
        budget = Budget(category=category, monthly_budget=monthly_budget)
        db.add(budget)
    db.commit()
    return {"ok": True, "message": f"Budget set for {category}: {format_currency(monthly_budget)}"}

@app.get("/budgets")
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.is_active == True).all()
    return [{"category": b.category, "monthly_budget": b.monthly_budget} for b in budgets]

@app.get("/spending-alerts")
def get_spending_alerts(db: Session = Depends(get_db)):
    alerts = []
    today = date.today()
    month_start = today.replace(day=1)
    
    monthly_spending = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total_spent')
        )
        .filter(Transaction.date >= month_start)
        .filter(Transaction.amount < 0)
        .group_by(Transaction.category)
        .all()
    )
    
    budgets = db.query(Budget).filter(Budget.is_active == True).all()
    budget_dict = {b.category: b.monthly_budget for b in budgets}
    
    for category, spent in monthly_spending:
        budget = budget_dict.get(category)
        if budget and abs(spent) > budget:
            overspend_percent = (abs(spent) - budget) / budget * 100
            alerts.append({
                "category": category,
                "budget": budget,
                "spent": abs(spent),
                "overspend_amount": abs(spent) - budget,
                "overspend_percent": overspend_percent
            })
    
    return alerts

# Multiple Users/Sessions Management
@app.post("/session/create")
def create_session(session_name: str = "Default Session", db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    session = UserSession(session_id=session_id, session_name=session_name)
    db.add(session)
    db.commit()
    return {"session_id": session_id, "session_name": session_name}

@app.get("/sessions")
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(UserSession).order_by(UserSession.last_activity.desc()).all()
    return [
        {
            "session_id": s.session_id,
            "session_name": s.session_name,
            "created_at": s.created_at.isoformat(),
            "last_activity": s.last_activity.isoformat(),
            "has_data": s.transactions_data is not None
        }
        for s in sessions
    ]

@app.post("/session/{session_id}/upload")
async def upload_to_session(session_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    global data_timestamp
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Process the CSV data
        expected = {"date", "description", "amount", "category"}
        df.columns = [c.strip().lower() for c in df.columns]

        if not expected.issubset(set(df.columns)):
            raise HTTPException(status_code=400, detail=f"CSV must have columns: {expected}")

        df['date'] = df['date'].apply(parse_csv_date)
        df['category'] = df['category'].fillna("Uncategorized").apply(normalize_category)
        df['merchant'] = df['description'].fillna("").apply(extract_merchant)
        df['amount'] = pd.to_numeric(df['amount'], errors="coerce")
        df = df.dropna(subset=["amount", "date"])

        # Store in session
        session.transactions_data = df.to_json()
        session.last_activity = datetime.utcnow()
        
        # Also update the main transactions table (for compatibility with other endpoints)
        records = [
            Transaction(
                date=row.date,
                description=row.description,
                merchant=row.merchant,
                amount=float(row.amount),
                category=row.category,
            )
            for row in df.itertuples(index=False)
        ]
        
        # Delete ALL transactions and replace with new ones
        db.query(Transaction).delete()
        db.add_all(records)
        db.commit()
        
        # Update timestamp to force frontend refresh
        data_timestamp = time.time()
        
        return {"ok": True, "rows": len(df), "session_id": session_id, "timestamp": data_timestamp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

@app.get("/session/{session_id}/analytics")
def get_session_analytics(session_id: str, db: Session = Depends(get_db)):
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not session or not session.transactions_data:
        raise HTTPException(status_code=404, detail="No data found for session")
    
    df = pd.read_json(session.transactions_data)
    
    # Calculate comprehensive analytics
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = df[df['amount'] < 0]['amount'].sum()
    net_balance = total_income + total_expenses
    
    category_summary = df.groupby('category')['amount'].sum().reset_index()
    monthly_summary = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
    monthly_summary['date'] = monthly_summary['date'].astype(str)
    
    return {
        "summary": {
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "net_balance": float(net_balance),
            "transaction_count": len(df)
        },
        "by_category": category_summary.to_dict('records'),
        "by_month": monthly_summary.to_dict('records'),
        "timestamp": data_timestamp
    }

@app.delete("/session/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"ok": True, "message": "Session deleted successfully"}

# -------------------------
# DEBUG ENDPOINTS
# -------------------------
@app.get("/debug/transactions")
def debug_transactions(limit: int = 10, db: Session = Depends(get_db)):
    """Debug endpoint to see what transactions are actually in the database"""
    transactions = db.query(Transaction).order_by(Transaction.date.desc()).limit(limit).all()
    
    return {
        "count": db.query(Transaction).count(),
        "transactions": [
            {
                "date": t.date.isoformat(),
                "description": t.description,
                "merchant": t.merchant,
                "amount": t.amount,
                "category": t.category
            }
            for t in transactions
        ],
        "timestamp": data_timestamp
    }

@app.delete("/debug/clear_all")
def debug_clear_all(db: Session = Depends(get_db)):
    """Debug endpoint to clear all transactions"""
    try:
        count = db.query(Transaction).count()
        db.query(Transaction).delete()
        db.commit()
        global data_timestamp
        data_timestamp = time.time()
        return {"ok": True, "message": f"All {count} transactions cleared", "timestamp": data_timestamp}
    except Exception as e:
        db.rollback()
        return {"ok": False, "error": str(e)}

# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    question = req.question.strip().lower()
    intent = classify_intent(question)
    start, end = parse_time_window(question, db)
    category = extract_category(question)

    query = db.query(Transaction)
    if start and end:
        query = query.filter(Transaction.date.between(start, end))
    if category:
        query = query.filter(func.lower(Transaction.category) == category.lower())

    if intent == "sum_by_category":
        total = query.with_entities(func.sum(Transaction.amount)).scalar() or 0.0
        verb = "earned" if total >= 0 else "spent"
        amount_str = format_currency(abs(total))
        time_range = f" from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}" if start and end else ""
        return ChatResponse(answer=f"You {verb} {amount_str} on {category}{time_range}")

    elif intent == "top_expenses":
        n = parse_topn(question)
        q = query.filter(Transaction.amount < 0)
        q = q.order_by(func.abs(Transaction.amount).desc()).limit(n).all()
        if not q:
            return ChatResponse(answer=f"No expenses found for the given criteria.")
        items = [{"label": f"{t.date} - {t.merchant}: {format_currency(t.amount)}", "value": float(t.amount)} for t in q]
        return ChatResponse(answer=f"Here are your top {len(items)} expenses:", data=items)

    elif intent == "spending_alerts":
        alerts = get_spending_alerts(db)
        if not alerts:
            return ChatResponse(answer="No spending alerts! You're within your budgets.")
        
        alert_messages = []
        for alert in alerts:
            message = f"{alert['category']}: Budget {format_currency(alert['budget'])}, Spent {format_currency(-alert['spent'])}, Overspent by {format_currency(alert['overspend_amount'])} ({alert['overspend_percent']:.1f}%)"
            alert_messages.append(message)
        
        return ChatResponse(answer="Spending Alerts:\n" + "\n".join(alert_messages))

    elif intent == "list_transactions":
        q = query.order_by(Transaction.date.desc()).limit(10).all()
        if not q:
            return ChatResponse(answer="No transactions found.")
        items = [{"label": f"{t.date} - {t.merchant}: {format_currency(t.amount)} ({t.category})", "value": float(t.amount)} for t in q]
        return ChatResponse(answer="Recent transactions:", data=items)

    else:
        if category:
            total = query.with_entities(func.sum(Transaction.amount)).scalar() or 0.0
            verb = "earned" if total >= 0 else "spent"
            amount_str = format_currency(abs(total))
            return ChatResponse(answer=f"You {verb} {amount_str} on {category} overall.")

        return ChatResponse(answer="I can help you analyze your spending. Try asking about specific categories or budgets.")