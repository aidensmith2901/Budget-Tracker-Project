import { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { PendingTasks } from './components/PendingTasks';
import { RecentExpenses } from './components/RecentExpenses';
import { QuickAccess } from './components/QuickAccess';
import { MonthlyReport } from './components/MonthlyReport';
import { DayToDayExpenses } from './components/DayToDayExpenses';
import { supabase } from './lib/supabase';
import './App.css';

// Default mock data when Supabase is not configured
const DEFAULT_TASKS = [
  { label: 'Pending Approvals', icon: 'bi-clock', value: 5 },
  { label: 'New Trips Registered', icon: 'bi-airplane', value: 1 },
  { label: 'Unreported Expenses', icon: 'bi-wallet2', value: 4 },
  { label: 'Upcoming Expenses', icon: 'bi-cart', value: 0 },
  { label: 'Unreported Advances', icon: 'bi-arrow-repeat', value: 0, isAmount: true },
];

const DEFAULT_EXPENSES = [
  { id: '1', subject: 'Office Supplies', employee: 'John Smith', team: 'Marketing', teamColor: 'blue' as const, amount: 150 },
  { id: '2', subject: 'Business Lunch', employee: 'Sarah Jade', team: '', teamColor: 'gray' as const, amount: 75.5 },
  { id: '3', subject: 'Travel Expenses', employee: 'Mike Brown', team: 'Operations', teamColor: 'red' as const, amount: 450.25 },
  { id: '4', subject: 'Client Dinner', employee: 'Jennifer Lee', team: 'Marketing', teamColor: 'blue' as const, amount: 120 },
  { id: '5', subject: 'Hotel', employee: 'David Wilson', team: 'Finance', teamColor: 'green' as const, amount: 275.75 },
];

const DEFAULT_TEAM_SPENDING = { labels: ['PO', 'S3', 'H9', 'IS', 'DW', 'HQ', 'B5'], data: [20, 45, 60, 35, 80, 55, 95] };
const DEFAULT_CATEGORY_EXPENSES = {
  labels: ['Accommodation', 'Comms', 'Services', 'Food', 'Fuel'],
  data: [75, 45, 60, 85, 40],
};

export default function App() {
  const [tasks, setTasks] = useState(DEFAULT_TASKS);
  const [expenses, setExpenses] = useState(DEFAULT_EXPENSES);
  const [teamSpending, setTeamSpending] = useState(DEFAULT_TEAM_SPENDING);
  const [categoryExpenses, setCategoryExpenses] = useState(DEFAULT_CATEGORY_EXPENSES);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const hasSupabase = import.meta.env.VITE_SUPABASE_URL && import.meta.env.VITE_SUPABASE_ANON_KEY;

    if (!hasSupabase) {
      setLoading(false);
      return;
    }

    async function fetchData() {
      try {
        // Fetch tasks from Supabase (if table exists)
        const { data: tasksData } = await supabase.from('tasks').select('*');
        if (tasksData?.length) {
          setTasks(
            tasksData.map((t) => ({
              label: t.type.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
              icon: 'bi-clock',
              value: t.amount ?? t.count,
              isAmount: t.type === 'unreported_advances',
            }))
          );
        }

        // Fetch expenses
        const { data: expensesData } = await supabase.from('expenses').select('*');
        if (expensesData?.length) {
          setExpenses(
            expensesData.map((e) => ({
              id: e.id,
              subject: e.subject,
              employee: e.employee_name,
              team: e.team_name,
              teamColor: (e.team_color ?? 'gray') as 'blue' | 'red' | 'green' | 'gray',
              amount: e.amount,
            }))
          );
        }

        // Fetch team spending for chart
        const { data: spendingData } = await supabase.from('team_spending').select('*');
        if (spendingData?.length) {
          const byCode = spendingData.reduce(
            (acc, row) => {
              acc.labels.push(row.team_code);
              acc.data.push(row.amount);
              return acc;
            },
            { labels: [] as string[], data: [] as number[] }
          );
          setTeamSpending(byCode);
        }

        // Fetch category expenses
        const { data: categoryData } = await supabase.from('category_expenses').select('*');
        if (categoryData?.length) {
          setCategoryExpenses({
            labels: categoryData.map((c) => c.category),
            data: categoryData.map((c) => c.percentage),
          });
        }
      } catch {
        // Keep default data on error
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="app">
        <Sidebar />
        <main className="main">
          <p style={{ color: 'var(--text-muted)' }}>Loading dashboard...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <div className="dashboard-grid">
          <PendingTasks tasks={tasks} />
          <RecentExpenses expenses={expenses} />
        </div>
        <div className="dashboard-grid full-width">
          <QuickAccess />
        </div>
        <div className="dashboard-grid">
          <MonthlyReport labels={teamSpending.labels} data={teamSpending.data} />
          <DayToDayExpenses labels={categoryExpenses.labels} data={categoryExpenses.data} />
        </div>
      </main>
    </div>
  );
}
