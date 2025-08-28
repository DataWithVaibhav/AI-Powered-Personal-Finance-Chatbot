# AI-Powered Personal Finance Chatbot

A full-stack web application that helps users analyze financial transactions through AI-powered insights and natural language queries. Upload CSV files, visualize spending patterns, and ask questions about your finances in plain English.

## 🚀 Features

- **CSV Upload & Processing**: Upload transaction data with automatic parsing and validation
- **AI-Powered Categorization**: Machine learning categorization of transactions using TF-IDF and Naive Bayes
- **Interactive Visualizations**: Multiple chart types including pie charts, bar charts, and trend analysis
- **Natural Language Chat Interface**: Ask questions about your finances using plain English
- **Budget Management**: Set monthly budgets by category and receive spending alerts
- **Multi-Session Support**: Manage different financial datasets with session management
- **Real-time Data Refresh**: Automatic UI updates when new data is uploaded

## 🛠️ Tech Stack

### Backend
- **FastAPI 0.104.1** - Modern, fast web framework for building APIs with Python
- **SQLAlchemy 2.0.23** - SQL toolkit and Object-Relational Mapping (ORM) library
- **SQLite** - Lightweight database for data storage
- **Pandas 2.1.3** - Data manipulation and analysis
- **Scikit-learn 1.3.2** - Machine learning for transaction categorization
- **Python 3.8+** - Programming language

### Frontend
- **React 18.3.1** - User interface library with hooks
- **Vite 5.4.2** - Fast build tool and development server
- **Axios 1.11.0** - HTTP client for API communication
- **Custom Components** - Framework-free UI components

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14 or higher** - [Download Node.js](https://nodejs.org/)
- **npm** - Package manager (comes with Node.js)
- **Modern web browser** - Chrome, Firefox, Safari, or Edge

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd AI-Powered-Personal-Finance-Chatbot

# Navigate to backend directory
cd backend
2. Backend Setup
bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database (creates transactions.db)
python -c "from db import Base, engine; Base.metadata.create_all(bind=engine)"

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
The backend server will start at http://localhost:8000

API Documentation: Visit http://localhost:8000/docs for interactive API documentation

3. Frontend Setup
bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
The frontend will be available at http://localhost:5173

4. Access the Application
Open your browser and go to http://localhost:5173 to start using the finance chatbot.


Column	Required	Description	Example
date	✅ Yes	Transaction date (multiple formats supported)	15-01-2024 or 2024-01-15
description	✅ Yes	Transaction description	AMAZON INDIA PVT LTD
amount	✅ Yes	Transaction amount (negative for expenses)	-2499.99
category	❌ Optional	Transaction category	Shopping, Food, Transport
Supported Date Formats
DD-MM-YYYY (01-04-2024)

YYYY-MM-DD (2024-04-01)

MM-DD-YYYY (04-01-2024)

DD-MM-YY (01-04-24)

Example CSV Content:
csv
date,description,amount,category
2024-01-15,Amazon Purchase,-2499.99,Shopping
2024-01-20,Salary Credit,50000.00,Income
2024-01-22,Restaurant Dinner,-1200.00,Food
2024-01-25,UBER *RIDE,-350.00,Transport

💬 Sample Chat Questions
Try these questions in the chat interface:

Spending Analysis
"How much did I spend on food last month?"

"Show me my top 5 expenses"

"What were my transportation costs in December?"

"How much have I spent at Amazon this year?"

🎯 API Endpoints
Core Endpoints
POST /upload_csv - Upload and process CSV file

GET /summary/by_category - Spending summary by category

GET /summary/top_merchants - Top merchants by spending

GET /summary/monthly_totals - Monthly spending totals

Visualization Endpoints
GET /visualization/category_pie - Data for category pie chart

GET /visualization/monthly_trend - Monthly income vs expenses trend

GET /visualization/top_merchants_by_total_spending - Top merchants by total spending

GET /visualization/top_merchants_by_single_payment - Largest individual transactions

GET /visualization/income_vs_expenses - Overall financial summary

Chat & Budget Management
POST /chat - Process natural language queries

POST /budgets - Set monthly budgets

GET /budgets - Get current budgets

GET /spending-alerts - Get budget violation alerts

Session Management
POST /session/create - Create new user session

GET /sessions - List all sessions

POST /session/{session_id}/upload - Upload data to specific session

GET /session/{session_id}/analytics - Get session analytics

DELETE /session/{session_id} - Delete session

Debug Endpoints
GET /debug/transactions - View transactions in database

DELETE /debug/clear_all - Clear all transaction data

🐛 Troubleshooting
Common Issues
CSV Upload Fails

Ensure your CSV has the required columns: date, description, amount, category

Check date formats match supported patterns

Verify file is not corrupted or empty

Backend Connection Issues

bash
# Check if backend is running
curl http://localhost:8000/
# Expected response: {"message":"🚀 AI Finance Chatbot Backend is running!"}
Frontend Connection Errors

Verify backend is running on port 8000

Check browser console for CORS errors

Ensure no firewall blocking localhost connections

Dependency Issues

bash
# Reinstall dependencies if needed
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
Database Issues

bash
# Reset database (deletes all data)
cd backend
python -c "from db import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
Debug Tools
Backend API Docs: http://localhost:8000/docs

Frontend Developer Tools: Browser console (F12)

Database Inspection: Use SQLite browser to inspect transactions.db

🔧 Development
Adding New Features
Backend Changes:

Add new endpoints in backend/main.py

Update models in backend/models.py if needed

Add utility functions in backend/utils.py

Frontend Changes:

Create new components in frontend/src/components/

Update API calls in frontend/src/api.js

Modify main app in frontend/src/App.jsx

Running Tests
bash
# Backend tests (add pytest to requirements.txt first)
cd backend
pytest

# Frontend tests (add testing library first)
cd frontend
npm test
📈 Performance Notes
Database indexes on frequently queried fields (date, category, merchant)

Efficient pandas operations for CSV processing

React memoization for expensive components

Proper API response caching headers

🔒 Security Considerations
Input validation on all API endpoints

SQL injection protection through SQLAlchemy ORM

CORS configured for development environment

No authentication (designed for local use only)

🚀 Deployment
Backend Deployment (Example: Railway)
bash
# Install railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway deploy
Frontend Deployment (Example: Vercel)
bash
# Install vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel --prod
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature-name

Make your changes and test thoroughly

Commit your changes: git commit -m 'Add new feature'

Push to the branch: git push origin feature-name

Submit a pull request

Development Guidelines
Follow PEP 8 for Python code

Use React best practices for frontend code

Write tests for new functionality

Update documentation for new features

📝 License
This project is open source and available under the MIT License.

🙋‍♂️ Support
If you encounter any issues:

Check the troubleshooting section above

Review the API documentation at http://localhost:8000/docs

Check browser console for frontend errors

Create an issue in the GitHub repository
