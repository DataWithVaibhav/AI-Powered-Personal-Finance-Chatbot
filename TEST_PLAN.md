📄 Finance Chatbot Test Plan
🧪 Testing Strategy

Testing Levels

Unit Testing: Verify individual functions and components

Integration Testing: Validate interactions between components and API endpoints

System Testing: End-to-end workflows from CSV upload to chat responses

Manual Testing: User experience, edge cases, and real-world scenarios

Test Environment

Backend: Python 3.8+, FastAPI, SQLite

Frontend: Node.js 14+, React 18, Chrome/Firefox browsers

Testing Tools: pytest, React Testing Library, manual testing

Test Data: Sample CSVs covering various formats, sizes, and edge cases

🔧 Unit Tests
Backend

CSV Processing Functions

def test_parse_csv_date():
    """Test date parsing with multiple formats and fallback"""
    assert parse_csv_date("15-01-2024") == date(2024,1,15)
    assert parse_csv_date("2024-01-15") == date(2024,1,15)
    assert parse_csv_date("01/15/2024") == date(2024,1,15)
    assert parse_csv_date("15-01-24") == date(2024,1,15)
    today = date.today()
    assert parse_csv_date("invalid-date") == today

def test_normalize_category():
    assert normalize_category("food") == "Food"
    assert normalize_category("GROCERIES") == "Food"
    assert normalize_category("uber ride") == "Transport"
    assert normalize_category("unknown") == "Unknown"

def test_extract_merchant():
    assert extract_merchant("AMAZON INDIA PVT LTD") == "Amazon India"
    assert extract_merchant("UBER *RIDE") == "Uber Ride"
    assert extract_merchant("") == "Unknown"
    assert extract_merchant("123!@#") == "Unknown"


AI Categorization Tests

def test_ai_categorization():
    """Test AI-based transaction categorization"""
    # Training data, unknown descriptions, fallback to rule-based
    # Model persistence and incremental learning

Frontend

API Client

test('uploadCsv handles errors', async () => {
  mockFetch.mockReject(new Error('Network error'));
  await expect(uploadCsv(testFile)).rejects.toThrow('Network error');
});

test('chat function formats request', async () => {
  await chat("How much spent on food?");
  expect(mockFetch).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
    method: 'POST',
    body: JSON.stringify({ question: "How much spent on food?" })
  }));
});


Component Tests

test('Uploader displays progress', () => { /* simulate upload, verify progress */ });
test('Chat handles budget input', async () => { /* verify API call and UI update */ });

🔗 Integration Tests

API Endpoint

def test_upload_csv_endpoint():
    client = TestClient(app)
    csv_data = "date,description,amount,category\n2024-01-15,Test Transaction,-100.0,Food"
    response = client.post("/upload_csv", files={"file": ("test.csv", csv_data, "text/csv")})
    assert response.status_code == 200
    assert response.json()["ok"] == True
    assert response.json()["rows"] == 1


Frontend-Backend Flow

test('upload and visualization', async () => {
  // Mock CSV upload, fetch chart data, verify rendering and refresh
});

📋 Manual Test Cases
CSV Upload
Test Case	Steps	Expected Result
Valid CSV	Select & upload file	Success, charts updated
Invalid CSV	Upload non-CSV	Error message
Missing Columns	Upload CSV missing 'amount'	Specific column error
Large File	Upload 10MB+	Progress indicator, success
Empty CSV	Upload empty file	Error message
Chat Functionality
Test Case	Steps	Expected Result
Category Spending	Ask "How much did I spend on food?"	Correct amount displayed
Top Expenses	Ask "Show my top 5 expenses"	List of 5 largest expenses
Time-based Query	Ask "Last month's transport spending"	Correct category amount
Unknown Query	Ask unrelated question	Graceful fallback
Budget Query	Ask "What's my budget for food?"	Correct budget displayed
Budget Management
Test Case	Steps	Expected Result
Set Budget	Select category, enter amount	Budget saved, confirmation
Budget Alert	Exceed budget	Alert triggered with overspend amount
Edit Budget	Change existing budget	Updated correctly
Invalid Budget	Enter negative amount	Error, not saved
🎯 Edge Cases

Data Processing

Empty CSV, missing values, mixed date formats

Negative/positive amounts, special characters, very large numbers

User Interaction

Rapid repeated uploads, network interruptions

Browser refresh during upload, very long chat questions

Large file handling with progress feedback

🚀 Performance Testing

Backend

CSV processing (1000+ rows <5s)

Database queries (<100ms, proper indexing)

API response (<200ms typical)

Concurrent users handling

Frontend

Bundle size <500KB gzipped

Smooth render (60fps)

Memory leak prevention

First contentful paint <1s

🔒 Security Testing

Input Validation

Prevent CSV injection, SQL injection, XSS, path traversal

Data Protection

No sensitive data leaks

Session isolation

Safe error messages

Proper CORS & API validation

📊 Test Data

valid_transactions.csv: Normal cases

missing_columns.csv: Column validation

large_file.csv: Performance test (10,000+ rows)

mixed_dates.csv: Date parsing

edge_cases.csv: Negative values, special characters

Chat Test Scenarios

test_questions = [
    ("How much spent on food?", "sum_by_category"),
    ("Show top expenses", "top_expenses"),
    ("Last month's transport", "time_category_query"),
    ("What's my budget?", "budget_query"),
    ("List recent transactions", "list_transactions"),
]

📝 Test Reporting

Metrics

Coverage >80% critical paths

Defect density <1/100 lines

API response, render times, memory usage

User acceptance & satisfaction

Bug Triage

Priorities: Critical, High, Medium, Low

Clear reproduction steps & expected vs actual

Verify fixes & regression testing

🔄 Regression Testing

Automated

Critical path tests on every commit (upload, chat, visualizations)

Full suite before releases

Cross-browser & device testing

Manual

CSV upload edge cases

All chart types render correctly

Chat responses & budget alerts

Session management, error handling, large datasets

🧪 User Acceptance Testing

Scenarios

First-time user onboarding

Power user advanced queries

Monthly spending review & export

Budget planning

Success Criteria

95%+ scenario completion

User satisfaction 4/5+

Operations <2s response

Error rate <5%

🚨 Known Issues & Limitations

No authentication (single-user only)

Basic NLP (pattern matching, limited AI)

Limited support for very large files >50MB

✅ Enhancements Made

Consolidated and structured all tests by level

Added performance & security focus

Clear edge cases and test scenarios

Streamlined reporting metrics
