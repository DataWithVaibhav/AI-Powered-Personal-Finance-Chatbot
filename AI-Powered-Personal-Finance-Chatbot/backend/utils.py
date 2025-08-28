# backend/utils.py
import re
from datetime import date, datetime, timedelta
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

# Category aliases for normalization and extraction
CATEGORY_ALIASES = {
    "food": ["food", "dining", "groceries", "restaurant", "cafe", "meal", "grocery", "snacks", "dinner", "lunch", "breakfast", "ccd"],
    "transport": ["transport", "transportation", "uber", "ola", "cab", "taxi", "fuel", "bus", "train", "metro", "petrol", "ride"],
    "shopping": ["shopping", "amazon", "flipkart", "myntra", "mall", "store", "clothing", "electronics", "purchase", "online"],
    "bills": ["bills", "utilities", "electricity", "wifi", "phone", "internet", "rent", "water", "mobile", "recharge", "bill"],
    "health": ["health", "doctor", "hospital", "pharmacy", "medicine", "healthcare", "gym"],
    "entertainment": ["entertainment", "movies", "cinema", "netflix", "game", "concert", "pvr", "ticket", "subscription", "movie"],
    "education": ["education", "school", "college", "tuition", "course", "udemy", "book"],
    "investment": ["investment", "stocks", "mutual fund", "dividend", "sip"],
    "income": ["salary", "income", "freelance", "bonus", "deposit", "payment"]
}

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
    """
    Parses a date string from the CSV into a Python date object.
    Tries common formats found in CSVs (DD-MM-YYYY, YYYY-MM-DD, MM/DD/YY).
    """
    date_str = date_str.strip().replace("/", "-")  # Handle slashes and dashes
    formats_to_try = [
        '%d-%m-%Y',  # 01-04-2024 (Your CSV's format)
        '%Y-%m-%d',  # 2024-04-01 (ISO format)
        '%m-%d-%Y',  # 04-01-2024 (US format)
        '%d-%m-%y',  # 01-04-24   (Short year)
    ]

    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue  # Try the next format if this one fails

    # If all parsing attempts fail, log a warning and use today's date
    print(f"Warning: Unable to parse date '{date_str}'. Using today's date as fallback.")
    return date.today()


def parse_time_window(q: str, db: Session = None) -> Tuple[Optional[date], Optional[date]]:
    """Parse time windows relative to the data in database, not current date"""
    ql = q.lower()
    
    # Get the latest date from the database to use as reference
    if db is not None:
        latest_date = db.query(func.max(Transaction.date)).scalar()
        if latest_date:
            today = latest_date
        else:
            today = date.today()
    else:
        today = date.today()

    # LAST MONTH (relative to latest data date)
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

    # THIS MONTH (of the latest transaction)
    if "this month" in ql:
        start = today.replace(day=1)
        if start.month == 12:
            end = date(start.year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(start.year, start.month + 1, 1) - timedelta(days=1)
        return start, end

    # THIS WEEK (relative to latest transaction)
    if "this week" in ql:
        start = today - timedelta(days=today.weekday())
        return start, start + timedelta(days=6)

    # LAST WEEK (relative to latest transaction)
    if "last week" in ql:
        start = today - timedelta(days=today.weekday() + 7)
        return start, start + timedelta(days=6)

    return None, None


def extract_category(q: str) -> Optional[str]:
    ql = q.lower()
    for k, vals in CATEGORY_ALIASES.items():
        if k in ql or any(v in ql for v in vals):
            return k.capitalize()
    # Additional pattern matching for better NLP
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
    
    # Improved pattern matching
    if any(word in ql for word in ["how much", "spent", "spend", "expense", "total", "amount"]) and extract_category(ql):
        return "sum_by_category"
    if "growing" in ql or "trend" in ql or "increase" in ql:
        return "fastest_growing_category"
    if any(word in ql for word in ["biggest", "top", "highest", "largest"]) and any(word in ql for word in ["expense", "spend", "purchase"]):
        return "top_expenses"
    if any(word in ql for word in ["list", "show", "what are", "which"]):
        return "list_transactions"
    return "fallback"