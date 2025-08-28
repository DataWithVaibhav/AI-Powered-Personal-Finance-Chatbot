📄 AI Tools Usage in Finance Chatbot
🤖 AI Tools Utilized
1. ChatGPT (OpenAI)

Purpose: Code generation, architecture design, debugging

Usage Pattern: Iterative prompts with code examples and errors

Key Contributions:

FastAPI backend endpoints

React component structures & state management

Database models with SQLAlchemy

Frontend API client & error handling

Validation and error handling logic

2. GitHub Copilot

Purpose: Inline code completion, boilerplate reduction

Usage Pattern: Suggestions and function generation

Key Contributions:

Utility functions & React hooks

CSS & layout suggestions

Error handling patterns

🎯 Prompt Strategies

Contextual Prompts: Provide project type, data structure, and expected behavior.
Example: CSV upload endpoint with multiple date formats, merchant extraction, category normalization, error handling, and response with row count.

Iterative Refinement: Build in versions, adding functionality step by step.
Example: Start with basic CSV parsing → multiple date formats → AI categorization → comprehensive error handling.

Error-Focused Prompts: Share specific errors to get targeted solutions.
Example: Handle pandas Unknown string format by trying multiple date formats.

Architecture Consultation: Ask for best practices on React + FastAPI with multi-chart visualization, chat interface, and session support.

💻 AI-Generated Code Validation
Validation Steps

Manual code review line by line

Functional testing with sample data

Integration testing of frontend-backend flow

Performance assessment

Modifications to AI Output

Enhanced date parsing and edge case handling

Added comprehensive error handling & validation

Cache-busting for data freshness

UI/UX refinements

Security hardening (input validation, SQL injection protection)

Performance optimization (queries & rendering)

📊 AI Contribution Levels
Area	AI Assistance
Boilerplate code, database models, utility functions	High (70-80%)
Business logic, API integration, chart components, state management	Moderate (40-60%)
Custom rules, UI/UX design, project architecture, performance optimization	Minimal (10-30%)
🔍 Specific AI-Generated Features

CSV Processing Endpoint: Handles multiple date formats, merchant extraction, category normalization, SQLite storage, and error handling.

NLP Categorization: TF-IDF + Naive Bayes classification with fallback to rules, supports incremental learning and model persistence.

React Visualization: Pie charts (category), line charts (income vs expenses), summary cards, top merchants bar chart with multiple views.

🧪 Testing AI Output

Unit tests for individual functions

Integration tests for component flow

Manual testing with real-world financial data

Edge case testing (empty files, unusual date formats, invalid data)

Common AI issues: missed edge cases, insufficient security & validation, performance inefficiencies, weak error handling.

📈 Lessons Learned

What Worked Well

Rapid prototyping & boilerplate reduction

Learning new patterns & approaches

Idea generation & coding consistency

Challenges

Context retention across multiple prompts

Output quality varies

Technical debt from quick fixes

Documentation gaps

Limited testing suggestions from AI

✅ Best Practices Developed

Always review AI code line by line

Use iterative, focused prompting

Test comprehensively

Maintain full understanding & ownership of code

Document AI-generated sections & assumptions

🚀 Future AI Integration Plans

Advanced NLP for chat

AI-assisted test & documentation generation

Performance optimization & refactoring

Accessibility improvements & ARIA labels

Localization support
