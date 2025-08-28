# Test Plan for Finance Chatbot

## 🧪 Testing Strategy

### Testing Levels
1. **Unit Testing**: Individual functions and components
2. **Integration Testing**: Component interactions and API endpoints
3. **System Testing**: End-to-end user workflows
4. **Manual Testing**: User experience and edge cases

### Test Environment
- **Backend**: Python 3.8+, FastAPI, SQLite
- **Frontend**: Node.js 14+, React 18, Chrome/Firefox browsers
- **Testing Tools**: pytest, React Testing Library, Manual testing
- **Test Data**: Sample CSV files with various formats and edge cases

## 🔧 Unit Tests

### Backend Unit Tests

#### CSV Processing Functions
```python
def test_parse_csv_date():
    """Test date parsing with various formats"""
    # Test multiple date formats
    assert parse_csv_date("15-01-2024") == date(2024, 1, 15)
    assert parse_csv_date("2024-01-15") == date(2024, 1, 15)
    assert parse_csv_date("01/15/2024") == date(2024, 1, 15)
    assert parse_csv_date("15-01-24") == date(2024, 1, 15)
    
    # Test invalid dates fallback to today
    today = date.today()
    assert parse_csv_date("invalid-date") == today

def test_normalize_category():
    """Test category normalization with aliases"""
    assert normalize_category("food") == "Food"
    assert normalize_category("GROCERIES") == "Food"
    assert normalize_category("uber ride") == "Transport"
    assert normalize_category("unknown") == "Unknown"

def test_extract_merchant():
    """Test merchant extraction from descriptions"""
    assert extract_merchant("AMAZON INDIA PVT LTD") == "Amazon India"
    assert extract_merchant("UBER *RIDE") == "Uber Ride"
    assert extract_merchant("") == "Unknown"
    assert extract_merchant("123!@#") == "Unknown"
AI Categorization Tests
python
def test_ai_categorization():
    """Test AI-based transaction categorization"""
    # Test with training data
    # Test with unknown descriptions
    # Test fallback to rule-based when no training data
    # Test model persistence and loading
Frontend Unit Tests
API Client Tests
javascript
test('uploadCsv handles errors properly', async () => {
  mockFetch.mockReject(new Error('Network error'));
  await expect(uploadCsv(testFile)).rejects.toThrow('Network error');
});

test('chat function formats request correctly', async () => {
  await chat("How much spent on food?");
  expect(mockFetch).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
    method: 'POST',
    body: JSON.stringify({ question: "How much spent on food?" })
  }));
});
Component Tests
javascript
test('Uploader displays progress during upload', () => {
  render(<Uploader onUploaded={mockCallback} />);
  // Simulate file selection and upload progress
  // Verify progress message updates
});

test('Chat component handles budget setting', async () => {
  render(<Chat />);
  // Test budget input and submission
  // Verify API call is made correctly
});
🔗 Integration Tests
API Endpoint Tests
python
def test_upload_csv_endpoint():
    """Test complete CSV upload workflow"""
    client = TestClient(app)
    
    # Create test CSV data
    csv_data = "date,description,amount,category\n2024-01-15,Test Transaction,-100.0,Food"
    
    # Mock file upload
    response = client.post("/upload_csv", files={"file": ("test.csv", csv_data, "text/csv")})
    
    assert response.status_code == 200
    assert response.json()["ok"] == True
    assert response.json()["rows"] == 1
    
    # Verify data actually inserted
    transactions = db.query(Transaction).all()
    assert len(transactions) == 1
    assert transactions[0].category == "Food"
Frontend-Backend Integration
javascript
test('complete upload and visualization flow', async () => {
  // Mock successful CSV upload
  // Mock subsequent data fetches for charts
  // Verify components render with correct data
  // Test that refresh callback works properly
});
📋 Manual Test Cases
CSV Upload Functionality
Test Case	Steps	Expected Result
Valid CSV Upload	1. Select valid CSV file
2. Click Upload	Success message, data appears in charts
Invalid CSV Format	1. Select non-CSV file
2. Click Upload	Error message displayed
Missing Required Columns	1. Upload CSV missing 'amount' column
2. Click Upload	Specific error about missing column
Large File Upload	1. Upload 10MB+ CSV file
2. Click Upload	Progress indicator, successful processing
Empty CSV File	1. Upload empty CSV
2. Click Upload	Error message about empty file
Chat Functionality
Test Case	Steps	Expected Result
Category Spending Query	Ask "How much did I spend on food?"	Correct amount displayed with time context
Top Expenses Query	Ask "Show my top 5 expenses"	List of 5 largest expenses with amounts
Time-based Query	Ask "Last month's transportation spending"	Amount for transport category in previous month
Unknown Query	Ask "What's the weather?"	Graceful fallback response
Budget Query	Ask "What's my budget for food?"	Current food budget amount displayed
Budget Management
Test Case	Steps	Expected Result
Set Budget	1. Select category
2. Enter amount
3. Click Set Budget	Budget appears in list, confirmation message
Budget Alert	1. Set low budget
2. Upload exceeding transactions
3. Check alerts	Spending alert generated with overspend amount
Edit Budget	1. Set new amount for existing category
2. Click Set Budget	Budget updated, old value replaced
Invalid Budget	1. Enter negative amount
2. Click Set Budget	Error message, budget not set
🎯 Edge Cases
Data Processing Edge Cases
Empty CSV files - Should handle gracefully with appropriate error

Mixed date formats - Should parse all supported formats correctly

Negative/Positive amounts - Should categorize appropriately (expenses vs income)

Special characters - Should handle in descriptions and merchant names

Very large numbers - Should format correctly in UI

Missing values - Should handle null/empty values appropriately

User Interaction Edge Cases
Rapid repeated uploads - Should handle gracefully without race conditions

Network interruptions - Should recover appropriately and show error states

Browser refresh during upload - Should not break application state

Very long chat questions - Should handle efficiently without performance issues

Large file uploads - Should show progress and not freeze UI

🚀 Performance Testing
Backend Performance
CSV Processing: Measure time for 1000+ row files (< 5 seconds)

Database Queries: Ensure indexes are used properly (< 100ms response)

API Response Times: All endpoints under 200ms for typical loads

Concurrent Users: Handle multiple simultaneous requests without degradation

Frontend Performance
Bundle Size: Keep under 500KB gzipped for fast loading

Render Performance: 60fps animations and smooth interactions

Memory Usage: No memory leaks with frequent data updates

Load Time: First contentful paint under 1 second

🔒 Security Testing
Input Validation
CSV Injection: Prevent malicious CSV content with proper validation

SQL Injection: ORM should prevent all injection attacks

XSS Prevention: Sanitize all user-generated content in responses

Path Traversal: Prevent file system access through uploads

Data Protection
Sensitive Data: No financial data leakage in error responses

Session Isolation: User sessions properly separated (when implemented)

Error Messages: No sensitive information in error responses

API Security: Proper CORS configuration and input validation

📊 Test Data
Sample CSV Files
valid_transactions.csv - Properly formatted test data with various categories

missing_columns.csv - Missing required columns for error testing

large_file.csv - 10,000+ rows for performance testing

mixed_dates.csv - Multiple date formats for parsing testing

edge_cases.csv - Negative values, special characters, edge cases

Chat Test Scenarios
python
test_questions = [
    ("How much spent on food?", "sum_by_category"),
    ("Show top expenses", "top_expenses"),
    ("Last month's transport", "time_category_query"),
    ("What's my budget?", "budget_query"),
    ("List recent transactions", "list_transactions"),
]
📝 Test Reporting
Metrics to Track
Test Coverage: >80% for critical code paths

Defect Density: <1 defect per 100 lines of code

Performance Metrics: API response times, render times, memory usage

User Acceptance: Manual testing success rate and user satisfaction

Bug Triage Process
Priority: Critical, High, Medium, Low based on impact

Reproduction Steps: Clear steps to reproduce the issue

Expected vs Actual: Document behavior differences

Fix Verification: Test fixes before closure and regression testing

🔄 Regression Testing
Automated Regression Suite
Critical Path Tests: Run on every commit (upload, chat, basic visualizations)

Full Test Suite: Run before releases and major changes

Browser Compatibility: Test on Chrome, Firefox, Safari, Edge

Mobile Responsiveness: Test on various screen sizes and devices

Manual Regression Checklist
CSV upload with various formats and edge cases

All chart types render correctly with sample data

Chat responses for key question types

Budget setting, editing, and alert generation

Session management and data isolation

Error handling and user-friendly messages

Performance with large datasets

Mobile responsiveness and touch interactions

🧪 User Acceptance Testing
Test Scenarios
First-time User: Onboarding and initial upload experience

Power User: Advanced queries and data analysis workflows

Data Review: Monthly spending review and export needs

Budget Planning: Setting and monitoring budgets effectively

Success Criteria
Task Completion: 95%+ of test scenarios completed successfully

User Satisfaction: 4/5+ rating on ease of use and functionality

Performance: All operations under 2 seconds response time

Error Rate: <5% of operations result in errors or issues

🚨 Known Issues and Limitations
Current Limitations
No User Authentication: Single-user system only

Basic NLP: Pattern matching instead of advanced AI