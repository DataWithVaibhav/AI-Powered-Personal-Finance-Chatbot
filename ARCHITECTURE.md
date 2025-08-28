Architecture Overview
System Design

The Finance Chatbot is a full-stack application with a React frontend and FastAPI backend, using SQLite for data storage. The architecture follows a modular design with clear separation of concerns.

High-Level Architecture
flowchart TD
    subgraph Frontend [React Frontend]
        A1[CSV Upload UI]
        A2[Chat Interface]
        A3[Charts & Visualizations]
    end

    subgraph Backend [FastAPI Backend]
        B1[CSV Upload Endpoint]
        B2[Chat Endpoint (NLP Intent Classification)]
        B3[Summary & Analytics API]
        B4[Visualization API]
        B5[Budget Management API]
    end

    subgraph Processing [Data Processing & AI]
        P1[Pandas Data Cleaning]
        P2[AI Categorization (TF-IDF + Naive Bayes)]
        P3[Rule-based Fallback Categorization]
    end

    subgraph Database [SQLite + SQLAlchemy ORM]
        D1[(Transactions Table)]
        D2[(Budgets Table)]
        D3[(UserSessions Table)]
    end

    A1 --> B1 --> P1 --> P2 --> D1
    A2 --> B2 --> D1
    A3 --> B3 --> D1
    A3 --> B4 --> D1
    A2 --> B5 --> D2
    B2 --> D3

Data Flow
1. CSV Upload & Processing

User CSV → FastAPI Upload Endpoint → Pandas Processing → AI Categorization → SQLite → Frontend Refresh

Steps:

User uploads CSV via React UI.

FastAPI validates and parses the CSV.

Pandas cleans/normalizes dates, merchants, categories.

AI (TF-IDF + Naive Bayes) categorizes uncategorized transactions.

Transactions stored in SQLite.

Frontend auto-refreshes with updated summaries and charts.

2. Chat Query Processing

User Query → NLP Classification → SQLAlchemy Query → Response Formatting → Frontend Display

Steps:

User asks: “How much did I spend on food last month?”

Intent classification (sum_by_category, top_expenses, etc.).

Entity/date range extraction.

Database query with filters.

Result formatted (currency, table, text summary).

3. Visualization Flow

Frontend Request → FastAPI Visualization API → SQLite Aggregation → JSON → React Charts

Charts include:

Category spending pie chart

Monthly income vs expenses trendline

Top merchants bar chart

Key Design Choices
Backend

FastAPI for async performance & auto-generated docs.

SQLAlchemy ORM with migrations-ready schema.

Pandas for efficient CSV parsing & aggregation.

Lightweight AI model (TF-IDF + Naive Bayes) for categorization.

Frontend

React with Hooks for modular components.

Minimal dependencies (Axios, chart libs).

Separation of concerns: Uploader, Chat, Charts as standalone components.

AI/ML

TF-IDF + Naive Bayes for low-resource categorization.

Rule-based fallback for safety.

Incremental learning for accuracy improvements.

Database Schema
Transactions
id INTEGER PRIMARY KEY
date DATE INDEXED
description TEXT
merchant TEXT INDEXED
amount FLOAT
category TEXT INDEXED

Budgets
id INTEGER PRIMARY KEY
category TEXT
monthly_budget FLOAT
is_active BOOLEAN
created_at DATETIME

UserSessions
id INTEGER PRIMARY KEY
session_id TEXT UNIQUE INDEXED
session_name TEXT
transactions_data JSON
created_at DATETIME
last_activity DATETIME

Trade-offs & Limitations

SQLite chosen for simplicity over PostgreSQL.

Basic NLP vs. advanced LLMs (time trade-off).

Local-only setup (no cloud hosting in prototype).

Simple UI (no Material-UI for speed).

Future Enhancements

JWT-based authentication & multi-user support.

Transformer-based NLP for better query understanding.

WebSocket live updates.

Bank API integrations for auto-sync.

Predictive analytics & forecasting.
