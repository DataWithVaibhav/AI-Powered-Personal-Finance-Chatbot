const API_BASE = "http://localhost:8000";

// A generic helper function to reduce repetition and improve error handling
async function fetchData(endpoint, options = {}) {
  try {
    let url = `${API_BASE}${endpoint}`;
    const finalOptions = { ...options }; // Create a mutable copy of options

    // --- AGGRESSIVE CACHE-BUSTING LOGIC START ---
    const method = finalOptions.method || 'GET';
    if (method.toUpperCase() === 'GET') {
      // 1. Add unique timestamp to URL
      const separator = url.includes('?') ? '&' : '?';
      url += `${separator}_=${new Date().getTime()}`;

      // 2. Add explicit no-cache headers to the request
      finalOptions.headers = {
        ...finalOptions.headers,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
      };
    }
    // --- AGGRESSIVE CACHE-BUSTING LOGIC END ---

    const res = await fetch(url, finalOptions);
    if (!res.ok) {
      console.error(`HTTP error! status: ${res.status} for endpoint: ${endpoint}`);
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const contentType = res.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
        return res.json();
    }
    return;

  } catch (error) {
    console.error(`Failed to fetch from ${endpoint}:`, error);
    throw error;
  }
}


export async function uploadCsv(file) {
  const fd = new FormData();
  fd.append("file", file);
  return fetchData('/upload_csv', {
    method: "POST",
    body: fd
  });
}

export function getByCategory() {
  return fetchData('/summary/by_category');
}

export function getTopMerchants(limit = 5) {
  return fetchData(`/summary/top_merchants?limit=${limit}`);
}

export function getMonthlyTotals() {
  return fetchData('/summary/monthly_totals');
}

export function getCategoryPieChart() {
  return fetchData('/visualization/category_pie');
}

export function getMonthlyTrendChart() {
  return fetchData('/visualization/monthly_trend');
}

export function getTopMerchantsByTotal(limit = 10) {
  return fetchData(`/visualization/top_merchants_by_total_spending?limit=${limit}`);
}

export function getTopMerchantsBySingle(limit = 10) {
  return fetchData(`/visualization/top_merchants_by_single_payment?limit=${limit}`);
}

export async function getIncomeVsExpenses() {
  try {
    return await fetchData('/visualization/income_vs_expenses');
  } catch (error) {
    return { totalIncome: 0, totalExpenses: 0, netSavings: 0 };
  }
}

export function setBudget(category, monthly_budget) {
  return fetchData(`/budgets?category=${encodeURIComponent(category)}&monthly_budget=${monthly_budget}`, {
    method: "POST"
  });
}

export function getBudgets() {
  return fetchData('/budgets');
}

export function deleteBudget(category) {
  return fetchData(`/budgets/${encodeURIComponent(category)}`, {
    method: "DELETE"
  });
}

export function getSpendingAlerts() {
  return fetchData('/spending-alerts');
}

export function chat(question) {
  return fetchData('/chat', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
}

export async function checkServerStatus() {
  try {
    const res = await fetch(`${API_BASE}/`);
    return res.ok;
  } catch (error) {
    console.error('Server not reachable:', error);
    return false;
  }
}

export function getSessionAnalytics(sessionId) {
  return fetchData(`/session/${sessionId}/analytics`);
}
