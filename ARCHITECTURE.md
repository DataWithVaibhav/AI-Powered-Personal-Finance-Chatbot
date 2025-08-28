## 📄 ARCHITECTURE.md

```markdown
# Architecture Overview

## System Design

The Finance Chatbot is a full-stack application with a React frontend and FastAPI backend, using SQLite for data storage. The architecture follows a modular design with clear separation of concerns.

## Data Flow

### 1. CSV Upload & Processing Pipeline
User CSV → FastAPI Upload Endpoint → Pandas Processing →
AI Categorization → SQLite Database → Frontend Refresh

text

**Detailed Steps:**
1. User uploads CSV file through React frontend
2. FastAPI receives file and validates structure
3. Pandas processes the CSV: date parsing, category normalization, merchant extraction
4. AI model categorizes uncategorized transactions using TF-IDF + Naive Bayes
5. Data stored in SQLite with SQLAlchemy ORM
6. Frontend automatically refreshes to display new data

### 2. Chat Query Processing
User Question → NLP Intent Classification → Database Query →
Response Generation → Formatted Answer

text

**Processing Steps:**
1. User submits natural language question
2. Intent classification identifies query type (sum_by_category, top_expenses, etc.)
3. Time window extraction for date-based queries
4. Category extraction from question text
5. Database query with appropriate filters
6. Response formatting with currency formatting

### 3. Visualization Data Flow
Frontend Request → API Endpoint → Database Aggregation →
JSON Response → React Component Rendering

text

## Key Design Choices

### Backend Architecture

**FastAPI Selection**: Chosen for its async capabilities, automatic API documentation, excellent performance, and easy integration with Python data science libraries.

**SQLAlchemy ORM**: Provides database abstraction, type safety, and future database migration capabilities. Allows switching from SQLite to PostgreSQL easily.

**Modular Structure**: Separated concerns with:
- `db.py`: Database configuration and session management
- `models.py`: SQLAlchemy data models with proper indexing
- `utils.py`: Business logic utilities and helper functions  
- `main.py`: API routes and application setup
- `schema.py`: Pydantic schemas for request/response validation

### Frontend Architecture

**React with Hooks**: Modern functional components with hooks for state management, providing better performance and cleaner code.

**Minimal Dependencies**: Only essential packages (React, Axios) to keep bundle size small and avoid dependency bloat.

**Component Structure**: 
- `Uploader.jsx`: File upload handling with progress indicators
- `Chat.jsx`: Natural language interface with budget management
- `Charts.jsx`: Data visualization components with multiple chart types

### AI/ML Integration

**TF-IDF + Naive Bayes**: Used for transaction categorization based on description text. Provides good accuracy with minimal training data.

**Incremental Learning**: Model retrains automatically as more categorized data becomes available, improving accuracy over time.

**Fallback System**: Rule-based categorization using category aliases when AI model isn't confident or available.

**Model Persistence**: Trained models saved to disk (`ai_category_model.pkl`, `ai_vectorizer.pkl`) for persistence across server restarts.

## Database Schema

### Transactions Table
```python
id: Integer (Primary Key)
date: Date (indexed)
description: String
merchant: String (indexed)
amount: Float
category: String (indexed)
Budgets Table
python
id: Integer (Primary Key)
category: String
monthly_budget: Float
is_active: Boolean
created_at: DateTime
UserSessions Table
python
id: Integer (Primary Key)
session_id: String (Unique, indexed)
session_name: String
transactions_data: String (JSON serialized data)
created_at: DateTime
last_activity: DateTime
API Design
RESTful Endpoints
POST /upload_csv - CSV file processing with multipart form data

GET /summary/* - Various summary endpoints with date filtering

GET /visualization/* - Chart data endpoints for frontend visualizations

POST /chat - Natural language queries with intent classification

POST /budgets - Budget management with validation

GET /spending-alerts - Budget violation detection

Response Format
json
{
  "data": [],
  "timestamp": 1234567890
}
Performance Optimizations
Database Indexing: Indexes on frequently queried fields (date, category, merchant) for faster queries.

Efficient Queries: SQLAlchemy optimized queries with proper aggregation and filtering.

Cache Busting: Frontend includes timestamp parameters to prevent browser caching of data.

Batch Processing: Efficient CSV processing with pandas vectorized operations.

Security Considerations
CORS Configuration: Enabled for development with wildcard origin (*)

Input Validation: Comprehensive validation on file uploads and API parameters

SQL Injection Protection: SQLAlchemy ORM prevents injection attacks

No Authentication: Designed for local use only - no user authentication implemented

Trade-offs and Limitations
Due to Time Constraints
No User Authentication: Single-user system only, no multi-user support

Basic NLP: Pattern matching instead of advanced NLP models like transformers

Local Storage Only: SQLite instead of production database like PostgreSQL

Simple UI: Custom components instead of UI framework like Material-UI

Technical Trade-offs
SQLite over PostgreSQL: Faster development setup, less scalability

TF-IDF over Transformers: Lighter weight, less accurate but faster

Client-side Rendering: Simpler implementation, less SEO-friendly

In-memory Processing: CSV processing in memory, limits file size

Future Enhancements
User Authentication: JWT-based multi-user support

Advanced NLP: Integration with LLMs for better understanding

Real-time Updates: WebSocket support for live data updates

Export Functionality: PDF/Excel reports generation

Mobile App: React Native version for mobile devices

Cloud Deployment: Docker containers and cloud database support

Advanced Analytics: Predictive spending trends and forecasting

Bank Integration: Direct bank API connections for automatic data sync