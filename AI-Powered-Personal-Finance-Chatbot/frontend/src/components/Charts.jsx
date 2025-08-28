import React from 'react'

// Main component now receives data as props from App.jsx
export default function Charts({
  categoryPie,
  monthlyTrend,
  incomeVsExpenses,
  topMerchantsByTotal,
  topMerchantsBySingle
}) {
  return (
    <div style={{ fontFamily: 'Segoe UI, Roboto, Arial, sans-serif' }}>
      <Section title="Financial Overview">
        <IncomeVsExpensesSummaryCard data={incomeVsExpenses} />
      </Section>
      
      <Section title="Spending by Category">
        <CategorySpendingTable data={categoryPie} />
      </Section>

      <Section title="Monthly Income vs. Expense">
        <MonthlyTrendTable data={monthlyTrend} />
      </Section>
      
      <Section title="Top Merchants (by Total Spending)">
        <BarChartVisual 
          title="Combined spending per merchant"
          labels={topMerchantsByTotal?.labels} 
          values={topMerchantsByTotal?.amounts}
        />
      </Section>

      <Section title="Largest Single Payments">
        <BarChartVisual 
          title="Biggest individual transactions"
          labels={topMerchantsBySingle?.labels} 
          values={topMerchantsBySingle?.amounts}
        />
      </Section>
    </div>
  )
}

// --- UI Components ---

function Section({ title, children }) {
  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: '8px', margin: '16px 0', backgroundColor: 'white' }}>
      <h3 style={{
        margin: 0,
        padding: '16px 24px',
        fontSize: '18px',
        fontWeight: '600',
        borderBottom: '1px solid #e0e0e0'
      }}>
        {title}
      </h3>
      <div style={{ padding: '16px 24px' }}>
        {children}
      </div>
    </div>
  )
}

function IncomeVsExpensesSummaryCard({ data }) {
  if (!data) return <div>Loading summary...</div>
  
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      gap: '24px',
      flexWrap: 'wrap',
      padding: '8px 0'
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '14px', color: '#666' }}>Total Income</div>
        <div style={{ color: '#2e7d32', fontSize: '22px', fontWeight: 'bold' }}>
          ₹{data.totalIncome?.toLocaleString('en-IN', {maximumFractionDigits: 0})}
        </div>
      </div>
      
      <div style={{ fontSize: '24px', color: '#999' }}>–</div>
      
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '14px', color: '#666' }}>Total Expenses</div>
        <div style={{ color: '#d32f2f', fontSize: '22px', fontWeight: 'bold' }}>
          ₹{data.totalExpenses?.toLocaleString('en-IN', {maximumFractionDigits: 0})}
        </div>
      </div>
      
      <div style={{ fontSize: '24px', color: '#999' }}>=</div>
      
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '14px', color: '#666' }}>Net Savings</div>
        <div style={{ 
          color: data.netSavings >= 0 ? '#2e7d32' : '#d32f2f', 
          fontSize: '22px', 
          fontWeight: 'bold' 
        }}>
          {data.netSavings >= 0 ? '+' : ''}₹{data.netSavings?.toLocaleString('en-IN', {maximumFractionDigits: 0})}
        </div>
      </div>
    </div>
  )
}

function MonthlyTrendTable({ data }) {
  if (!data || !data.months || data.months.length === 0) {
    return <div style={{ color: '#666' }}>No monthly data available.</div>
  }

  const monthlySummary = data.months.map((month, index) => ({
    month,
    income: data.income[index],
    expenses: data.expenses[index],
    net: data.income[index] - data.expenses[index]
  }))

  return (
    <div>
      {monthlySummary.map((item, index) => (
        <div 
          key={item.month} 
          style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            padding: '16px 0',
            borderBottom: index < monthlySummary.length - 1 ? '1px solid #f0f0f0' : 'none',
          }}
        >
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#333' }}>{item.month}</div>
          <div style={{ display: 'flex', gap: '32px', fontSize: '15px' }}>
            <div style={{ minWidth: '130px', textAlign: 'right' }}>
              <span style={{ color: '#2e7d32', fontWeight: '600' }}>Income: </span>
              ₹{item.income?.toLocaleString('en-IN')}
            </div>
            <div style={{ minWidth: '130px', textAlign: 'right' }}>
              <span style={{ color: '#d32f2f', fontWeight: '600' }}>Expense: </span>
              ₹{item.expenses?.toLocaleString('en-IN')}
            </div>
            <div style={{ minWidth: '130px', textAlign: 'right' }}>
              <span style={{ fontWeight: '600', color: '#333' }}>Net: </span>
              <span style={{ color: item.net >= 0 ? '#2e7d32' : '#d32f2f' }}>
                {item.net >= 0 ? '+' : ''}₹{item.net?.toLocaleString('en-IN')}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

function CategorySpendingTable({ data }) {
  if (!data || !data.labels || data.labels.length === 0) {
    return <div style={{ color: '#666' }}>No category spending data available.</div>
  }

  const categorySummary = data.labels
    .map((label, index) => ({
      label,
      value: data.values[index],
      color: data.colors[index % data.colors.length]
    }))
    .filter(item => item.value > 0)
    .sort((a, b) => b.value - a.value)

  return (
    <div>
      {categorySummary.map((item, index) => (
        <div key={item.label} style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          padding: '12px 0',
          borderBottom: index < categorySummary.length - 1 ? '1px solid #f0f0f0' : 'none',
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{
              width: '12px',
              height: '12px',
              backgroundColor: item.color || '#ccc',
              marginRight: '12px',
              borderRadius: '3px'
            }}></div>
            <span style={{ fontWeight: '500', fontSize: '15px', color: '#333' }}>{item.label}</span>
          </div>
          <span style={{ fontFamily: 'monospace', fontSize: '16px', fontWeight: '600' }}>
            ₹{item.value?.toLocaleString('en-IN')}
          </span>
        </div>
      ))}
    </div>
  )
}

function BarChartVisual({ title, labels, values }) {
  if (!labels || !values || labels.length === 0) {
    return <div style={{ color: '#666' }}>No data available for this chart.</div>
  }
  
  const numericValues = values.map(val => Number(String(val).replace(/[^0-9.-]+/g, "")) || 0)
  const maxValue = Math.max(...numericValues)
  
  if (maxValue === 0) {
    return <div style={{ color: '#666' }}>No spending data available for this chart.</div>
  }
  
  return (
    <div>
      <h4>{title}</h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '16px' }}>
        {labels.map((label, index) => {
          const value = numericValues[index]
          const percentage = maxValue > 0 ? (value / maxValue) * 100 : 0
          
          return (
            <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ width: '150px', fontSize: '14px', fontWeight: 500, flexShrink: 0, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{label}</span>
              <div style={{ flexGrow: 1, backgroundColor: '#f0f0f0', borderRadius: '4px', height: '24px' }}>
                <div style={{
                  height: '100%',
                  backgroundColor: '#0288d1',
                  width: `${percentage}%`,
                  borderRadius: '4px',
                  minWidth: '4px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-end',
                  paddingRight: '8px',
                  color: 'white',
                  fontSize: '12px',
                  fontWeight: 'bold',
                  boxSizing: 'border-box'
                }}>
                  ₹{value.toLocaleString('en-IN', {maximumFractionDigits: 0})}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
