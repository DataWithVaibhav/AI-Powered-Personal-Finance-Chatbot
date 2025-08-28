import React, { useEffect, useState } from 'react'
import Uploader from './components/Uploader'
import Chat from './components/Chat'
import Charts from './components/Charts'
import {
  getByCategory,
  getTopMerchants,
  getMonthlyTotals,
  getCategoryPieChart,
  getMonthlyTrendChart,
  getIncomeVsExpenses,
  getTopMerchantsByTotal,
  getTopMerchantsBySingle
} from './api'

export default function App() {
  const [byCategory, setByCategory] = useState([])
  const [topMerchants, setTopMerchants] = useState([])
  const [monthlyTotals, setMonthlyTotals] = useState([])
  const [categoryPie, setCategoryPie] = useState(null)
  const [monthlyTrend, setMonthlyTrend] = useState(null)
  const [incomeVsExpenses, setIncomeVsExpenses] = useState(null)
  const [topMerchantsByTotal, setTopMerchantsByTotal] = useState(null)
  const [topMerchantsBySingle, setTopMerchantsBySingle] = useState(null)

  const refresh = async () => {
    try {
      const [
        byCat,
        merchants,
        monthly,
        pie,
        trend,
        incomeVsExp,
        merchantsByTotal,
        merchantsBySingle
      ] = await Promise.all([
        getByCategory(),
        getTopMerchants(),
        getMonthlyTotals(),
        getCategoryPieChart(),
        getMonthlyTrendChart(),
        getIncomeVsExpenses(),
        getTopMerchantsByTotal(),
        getTopMerchantsBySingle()
      ])

      setByCategory(byCat)
      setTopMerchants(merchants)
      setMonthlyTotals(monthly)
      setCategoryPie(pie)
      setMonthlyTrend(trend)
      setIncomeVsExpenses(incomeVsExp)
      setTopMerchantsByTotal(merchantsByTotal)
      setTopMerchantsBySingle(merchantsBySingle)
    } catch (err) {
      console.error("Error refreshing data:", err)
    }
  }

  // Load data once at startup
  useEffect(() => { refresh() }, [])

  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16, fontFamily: 'system-ui, sans-serif' }}>
      <h1>AI-Powered Personal Finance Chatbot</h1>
      <p style={{ color: '#666' }}>Upload your transactions CSV, see insights, and ask questions.</p>

      {/* Upload CSV and auto-refresh data */}
      <Uploader onUploaded={refresh} />

      <h2>Summaries</h2>
      <Charts
        categoryPie={categoryPie}
        monthlyTrend={monthlyTrend}
        incomeVsExpenses={incomeVsExpenses}
        topMerchantsByTotal={topMerchantsByTotal}
        topMerchantsBySingle={topMerchantsBySingle}
      />

      <h2>Chat</h2>
      <Chat />

      <footer style={{ marginTop: 32, fontSize: 12, color: '#999' }}>
        Demo app · Built with React + FastAPI + SQLite
      </footer>
    </div>
  )
}
