import React, { useEffect, useState } from "react";
import { setBudget as apiSetBudget, getBudgets, chat as apiChat } from "../api";

const categories = [
  "Food",
  "Transport",
  "Shopping",
  "Entertainment",
  "Bills",
  "Education",
  "Health",
  "Investment",
  "Other",
];

export default function Chat() {
  const [category, setCategory] = useState("Food");
  const [monthlyBudget, setMonthlyBudget] = useState("5000");
  const [budgets, setBudgets] = useState([]);

  const [question, setQuestion] = useState("How much did I spend on food last month?");
  const [answer, setAnswer] = useState("");
  const [loadingAsk, setLoadingAsk] = useState(false);
  const [savingBudget, setSavingBudget] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadBudgets();
  }, []);

  const loadBudgets = async () => {
    try {
      const data = await getBudgets();
      setBudgets(Array.isArray(data) ? data : data?.budgets || []);
    } catch (e) {
      setError("Could not load budgets.");
      console.error(e);
    }
  };

  const handleSetBudget = async () => {
    const value = Number(monthlyBudget);
    if (!value || value <= 0) {
      setError("Please enter a valid monthly budget.");
      return;
    }
    setError("");
    try {
      setSavingBudget(true);
      await apiSetBudget(category, value);

      // ✅ Update instantly in UI
      setBudgets((prev) => {
        const updated = prev.filter((b) => (b.category || b[0]) !== category);
        return [...updated, { category, monthly_budget: value }];
      });

      // Then sync with backend
      await loadBudgets();
    } catch (e) {
      setError("Failed to set budget.");
      console.error(e);
    } finally {
      setSavingBudget(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoadingAsk(true);
    setError("");
    try {
      const data = await apiChat(question.trim());
      const msg = data?.answer || data?.response || data?.message || "No answer.";
      setAnswer(msg);
    } catch (e) {
      setError("Chat failed. Please try again.");
      console.error(e);
    } finally {
      setLoadingAsk(false);
    }
  };

  return (
    <div style={{
      background: "white",
      borderRadius: "16px",
      boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
      padding: "24px",
      marginTop: "20px"
    }}>
      <h2 style={{ margin: 0, marginBottom: "16px", fontSize: "20px", fontWeight: "700", color: "#0d47a1" }}>
        💰 Budget & Chat
      </h2>

      {/* Budget Section */}
      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", marginBottom: "16px" }}>
        {/* Custom Dropdown Component */}
        <div style={{
          position: "relative",
          display: "inline-block",
          minWidth: "150px",
          flex: "1"
        }}>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            style={{
              width: "100%",
              padding: "12px 14px",
              fontSize: "18px",
              border: "1px solid #ccc",
              borderRadius: "10px",
              backgroundColor: "white",
              color: "black",
              cursor: "pointer",
              appearance: "none",
              WebkitAppearance: "none",
              MozAppearance: "none"
            }}
          >
            {categories.map((c) => (
              <option 
                key={c} 
                value={c}
                style={{ 
                  fontSize: "18px",
                  padding: "10px"
                }}
              >
                {c}
              </option>
            ))}
          </select>
          {/* Dropdown arrow indicator */}
          <div style={{
            position: "absolute",
            right: "14px",
            top: "50%",
            transform: "translateY(-50%)",
            pointerEvents: "none",
            fontSize: "18px",
            color: "#666"
          }}>
            ▼
          </div>
        </div>

        <input
          type="number"
          value={monthlyBudget}
          onChange={(e) => setMonthlyBudget(e.target.value)}
          placeholder="Monthly budget"
          style={{
            width: "160px",
            padding: "12px 14px",
            border: "1px solid #ccc",
            borderRadius: "10px",
            fontSize: "16px"
          }}
        />

        <button
          onClick={handleSetBudget}
          disabled={savingBudget}
          style={{
            background: "#1976d2",
            color: "white",
            border: "none",
            borderRadius: "10px",
            padding: "12px 20px",
            fontSize: "16px",
            fontWeight: "600",
            cursor: "pointer",
            flexShrink: 0
          }}
        >
          {savingBudget ? "Saving…" : "Set Budget"}
        </button>
      </div>

      {/* Budgets Table */}
      <BudgetsTable budgets={budgets} />

      {/* Chat Section */}
      <div style={{
        marginTop: "20px",
        borderTop: "1px solid #eee",
        paddingTop: "20px"
      }}>
        <div style={{ display: "flex", gap: "12px" }}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask something about your spending…"
            style={{
              flex: 1,
              padding: "14px 16px",
              fontSize: "16px",
              border: "1px solid #ccc",
              borderRadius: "12px"
            }}
          />
          <button
            onClick={handleAsk}
            disabled={loadingAsk}
            style={{
              background: "#2e7d32",
              color: "white",
              border: "none",
              borderRadius: "12px",
              padding: "14px 24px",
              fontSize: "16px",
              fontWeight: "700",
              cursor: "pointer",
              whiteSpace: "nowrap"
            }}
          >
            {loadingAsk ? "Asking…" : "Ask"}
          </button>
        </div>

        {error && <div style={{ color: "#d32f2f", marginTop: 12 }}>{error}</div>}

        {answer && (
          <div style={{
            marginTop: "16px",
            background: "#f5f5f5",
            padding: "12px 16px",
            borderRadius: "10px",
            fontSize: "15px"
          }}>
            <strong>Answer: </strong>{answer}
          </div>
        )}
      </div>
    </div>
  );
}

function BudgetsTable({ budgets }) {
  if (!budgets || budgets.length === 0) {
    return <div style={{ color: "#777", marginBottom: "8px" }}>No budgets set yet.</div>;
  }
  return (
    <div style={{
      border: "1px solid #e0e0e0",
      borderRadius: "12px",
      overflow: "hidden",
      marginTop: "12px"
    }}>
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        background: "#f1f8ff",
        padding: "10px 14px",
        fontWeight: "600"
      }}>
        <div>Category</div>
        <div style={{ textAlign: "right" }}>Budget</div>
      </div>
      {budgets.map((b, i) => (
        <div key={i} style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          padding: "10px 14px",
          borderTop: "1px solid #eee"
        }}>
          <div>{b.category || b[0]}</div>
          <div style={{ textAlign: "right", fontWeight: "600", color: "#1976d2" }}>
            ₹{Number(b.monthly_budget ?? b[1]).toLocaleString("en-IN")}
          </div>
        </div>
      ))}
    </div>
  );
}