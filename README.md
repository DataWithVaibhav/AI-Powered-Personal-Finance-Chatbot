💰 AI-Powered Personal Finance Chatbot

A smart personal finance assistant that helps you understand your spending without scrolling endlessly through statements. Just upload your bank/expense CSV, and the chatbot will summarize your expenses, show breakdowns, and answer your financial questions in plain English.

Think of it as your personal finance buddy:

💬 “How much did I spend on food last month?”
📊 “Show me my top 5 expenses.”
💸 “Summarize my biggest 3 payments this week.”

You’ll get tables, bar charts, and chatbot answers instantly.

🚀 Key Features

✅ Upload & Process CSVs – Upload your bank/expense data, automatically cleaned & validated.
✅ AI Categorization – No categories in your CSV? The app uses ML (TF-IDF + Naive Bayes) to guess them.
✅ Visual Insights – Category breakdowns, income vs expenses, top merchants, and largest transactions.
✅ Natural Language Chat – Ask financial questions like you’d ask a friend.
✅ Budget Alerts – Set a budget and get notified if you cross limits.
✅ Session Management – Track multiple datasets (personal, family, or business).
✅ Real-Time Refresh – Charts and tables update instantly when new data is uploaded.

🛠️ Tech Stack
Backend

⚡ FastAPI – Super-fast Python API
🗄️ SQLite – Lightweight database
📊 Pandas + Scikit-learn – Data analysis + ML for categorization

Frontend

⚛️ React (with Vite) – Fast, modern UI
📡 Axios – For backend communication
🎨 Custom Components – Clean, simple design

📋 Before You Start

Make sure you have:

Python 3.8+ → Download

Node.js 14+ (with npm) → Download

A modern browser (Chrome, Firefox, Edge, etc.)

Your expenses CSV file 🗂️

🚀 Quick Start
1️⃣ Clone & Setup
git clone https://github.com/DataWithVaibhav/AI-Powered-Personal-Finance-Chatbot
cd AI-Powered-Personal-Finance-Chatbot

2️⃣ Backend (FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "from db import Base, engine; Base.metadata.create_all(bind=engine)"
uvicorn main:app --reload --host 0.0.0.0 --port 8000


Backend runs at 👉 http://localhost:8000

Interactive docs 👉 http://localhost:8000/docs

3️⃣ Frontend (React)
cd frontend
npm install
npm run dev


Frontend runs at 👉 http://localhost:5173

📊 CSV Format
Column	Required	Description	Example
date	✅ Yes	Transaction date	2024-01-15
description	✅ Yes	Merchant / Transaction description	Amazon India Pvt Ltd
amount	✅ Yes	Transaction amount (negative = expense, positive = income)	-2499.99
category	❌ No	Spending category (auto-detected if missing)	Shopping

Example CSV:

date,description,amount,category
2024-01-15,Amazon Purchase,-2499.99,Shopping
2024-01-20,Salary Credit,50000.00,Income
2024-01-22,Restaurant Dinner,-1200.00,Food
2024-01-25,UBER *RIDE,-350.00,Transport

💬 Sample Chat Prompts

“How much did I spend on food last month?”

“Show me my top  expenses.”

“Show Total bill?”

“Show me last month bill?”

📈 Visual Insights

Spending by Category (table) – Breakdown of expenses per category

Monthly Income vs Expenses (table) – Net calculation with income & expense totals

Top Merchants (bar chart) – Biggest merchants by total spending

Largest Transactions (bar chart) – Highest-value single payments

🐛 Troubleshooting

CSV Upload Fails? → Check if your file has at least date, description, amount columns.

Backend not connecting? → Make sure FastAPI is running on port 8000.

Database issues? → Reset with:

cd backend
python -c "from db import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"

🔒 Security Considerations

Input validation for uploads

SQL injection protection via SQLAlchemy ORM

CORS enabled for dev use

❌ No authentication (local demo app only)

🎥 Demo

📹 A quick demo video is included in the repo → AI-Powered-Personal-Finance-Chatbot.mp4

👨‍💻 Author

Vaibhav Singh
📧 vaibhav0817@gmail.com
