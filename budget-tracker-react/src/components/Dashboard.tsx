import { useState, useEffect } from 'react';
import type { Category, Transaction } from '../types';
import { loadTransactions } from '../storage';
import { AccountsSection } from './AccountsSection';
import { TransactionsSection } from './TransactionsSection';
import { SummaryChart } from './SummaryChart';
import './Dashboard.css';

interface DashboardProps {
  categories: Category[];
}

export function Dashboard({ categories }: DashboardProps) {
  const [transactions, setTransactions] = useState<Transaction[]>(() => loadTransactions());
  const [selectedAccount, setSelectedAccount] = useState<string>('all');
  const [chartView, setChartView] = useState<'month' | 'year' | 'budget-actual'>('month');

  useEffect(() => {
    // Save transactions when they change
    const { saveTransactions } = require('../storage');
    saveTransactions(transactions);
  }, [transactions]);

  const accounts = [
    { name: 'Bank Account', balance: 23826 },
    { name: 'Vaults', balance: 34109 },
    { name: 'Cash', balance: 10320 },
  ];

  const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0);

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <nav className="nav">
          <a href="#" className="nav-link">
            <i className="bi bi-currency-euro"></i> Transactions
          </a>
          <a href="#" className="nav-link">
            <i className="bi bi-file-earmark-text"></i> Invoices
          </a>
          <a href="#" className="nav-link">
            <i className="bi bi-graph-up"></i> Reports
          </a>
          <a href="#" className="nav-link">
            <i className="bi bi-calendar3"></i> Calendar
          </a>
          <a href="#" className="nav-link">
            <i className="bi bi-building"></i> Company and users
          </a>
        </nav>
        <div className="sidebar-footer">
          <p className="sidebar-label">Total on your accounts</p>
          <p className="sidebar-total">€{totalBalance.toLocaleString()}</p>
        </div>
      </aside>

      {/* Main content */}
      <main className="main">
        <header className="header">
          <div className="brand">
            <span className="brand-icon">
              <i className="bi bi-search"></i>
              <i className="bi bi-currency-euro"></i>
            </span>
            <span className="brand-name">FinPlanner</span>
          </div>
          <div className="header-actions">
            <button type="button" className="icon-btn" aria-label="Account">
              <i className="bi bi-person"></i>
            </button>
            <button type="button" className="icon-btn" aria-label="Help">
              <i className="bi bi-question-circle"></i>
            </button>
            <button type="button" className="icon-btn" aria-label="Settings">
              <i className="bi bi-gear"></i>
            </button>
          </div>
        </header>

        <div className="content">
          <h1 className="welcome">Welcome!</h1>

          {/* My accounts */}
          <AccountsSection accounts={accounts} />

          {/* Recent transactions */}
          <TransactionsSection
            transactions={transactions}
            selectedAccount={selectedAccount}
            onAccountChange={setSelectedAccount}
            categories={categories}
          />

          {/* Summary chart */}
          <SummaryChart
            view={chartView}
            onViewChange={setChartView}
            transactions={transactions}
            categories={categories}
          />
        </div>
      </main>
    </div>
  );
}
