/**
 * Dashboard: account filter for transactions, chart view switching (month / year / budget vs actual).
 * Uses Chart.js for the bottom graphic.
 */

(function () {
  "use strict";

  // ----- Recent transactions (filterable by account) -----
  const transactions = [
    { date: "14/11/23", amount: 2011, company: "Company Co.", category: "Stocks", account: "Bank Account" },
    { date: "14/11/23", amount: -690, company: "Acme", category: "Subscriptions", account: "Bank Account" },
    { date: "15/11/23", amount: -120, company: "Streamio", category: "Supplies", account: "Vaults" },
    { date: "16/11/23", amount: 500, company: "Investr", category: "Investment", account: "Vaults" },
    { date: "17/11/23", amount: -45, company: "Coffee Shop", category: "Food", account: "Cash" },
    { date: "18/11/23", amount: 3200, company: "Employer", category: "Salary", account: "Bank Account" },
    { date: "19/11/23", amount: -89, company: "Utility Co.", category: "Bills", account: "Bank Account" },
    { date: "20/11/23", amount: -200, company: "Gym", category: "Subscriptions", account: "Vaults" },
  ];

  const accountFilter = document.getElementById("transaction-account-filter");
  const tbody = document.getElementById("transactions-tbody");
  const emptyRow = document.getElementById("transactions-empty");

  function formatAmount(amount) {
    const sign = amount >= 0 ? "+" : "";
    return sign + "€" + Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }

  function renderTransactions(accountKey) {
    const filtered =
      !accountKey || accountKey === "all"
        ? transactions
        : transactions.filter(function (t) {
            return t.account === accountKey;
          });

    if (emptyRow) emptyRow.classList.toggle("hidden", filtered.length > 0);

    if (!tbody) return;
    tbody.innerHTML = "";

    filtered.forEach(function (t) {
      const tr = document.createElement("tr");
      tr.setAttribute("data-account", t.account);
      tr.innerHTML =
        "<td>" +
        t.date +
        "</td>" +
        '<td class="' +
        (t.amount >= 0 ? "amount-in" : "amount-out") +
        '">' +
        formatAmount(t.amount) +
        "</td>" +
        "<td>" +
        escapeHtml(t.company) +
        "</td>" +
        "<td><span class=\"tag\">" +
        escapeHtml(t.category) +
        "</span></td>";
      tbody.appendChild(tr);
    });
  }

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  if (accountFilter) {
    accountFilter.addEventListener("change", function () {
      renderTransactions(this.value);
    });
  }

  renderTransactions(accountFilter ? accountFilter.value : "all");

  // ----- Chart (summary this month / this year / budget vs actual) -----
  const chartCanvas = document.getElementById("summary-chart");
  if (!chartCanvas) return;

  const ChartLib = window.Chart;
  if (!ChartLib) return;

  const incomeColor = "rgba(74, 124, 89, 0.9)";
  const expensesColor = "rgba(143, 184, 150, 0.9)";
  const budgetColor = "rgba(100, 120, 140, 0.6)";
  const actualColor = "rgba(74, 124, 89, 0.9)";

  let summaryChart = null;

  function destroyChart() {
    if (summaryChart) {
      summaryChart.destroy();
      summaryChart = null;
    }
  }

  function renderThisMonth() {
    destroyChart();
    summaryChart = new ChartLib(chartCanvas, {
      type: "bar",
      data: {
        labels: ["Income", "Expenses"],
        datasets: [
          {
            label: "Amount (€)",
            data: [4200, 2840],
            backgroundColor: [incomeColor, expensesColor],
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Summary this month" },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { callback: (v) => "€" + v.toLocaleString() },
          },
        },
      },
    });
  }

  function renderThisYear() {
    destroyChart();
    summaryChart = new ChartLib(chartCanvas, {
      type: "bar",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
        datasets: [
          {
            label: "Income",
            data: [3200, 3400, 3100, 3500, 3300, 3600, 3400, 3200, 3500, 3800, 4200],
            backgroundColor: incomeColor,
            borderRadius: 4,
          },
          {
            label: "Expenses",
            data: [2400, 2600, 2500, 2700, 2550, 2800, 2650, 2400, 2700, 2900, 2840],
            backgroundColor: expensesColor,
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Summary this year (monthly)" },
        },
        scales: {
          y: {
            beginAtZero: true,
            stacked: false,
            ticks: { callback: (v) => "€" + v.toLocaleString() },
          },
          x: { stacked: false },
        },
      },
    });
  }

  function renderBudgetVsActual() {
    destroyChart();
    summaryChart = new ChartLib(chartCanvas, {
      type: "bar",
      data: {
        labels: ["Food", "Bills", "Subscriptions", "Transport", "Savings"],
        datasets: [
          {
            label: "Budget (€)",
            data: [400, 350, 120, 180, 500],
            backgroundColor: budgetColor,
            borderRadius: 4,
          },
          {
            label: "Actual (€)",
            data: [380, 320, 135, 165, 480],
            backgroundColor: actualColor,
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Budget vs actual by category" },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { callback: (v) => "€" + v.toLocaleString() },
          },
        },
      },
    });
  }

  const viewHandlers = {
    month: renderThisMonth,
    year: renderThisYear,
    "budget-actual": renderBudgetVsActual,
  };

  function setChartView(viewKey) {
    const fn = viewHandlers[viewKey];
    if (fn) fn();
  }

  const chartFilterButtons = document.querySelectorAll("[data-chart-view]");
  chartFilterButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const view = this.getAttribute("data-chart-view");
      chartFilterButtons.forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      setChartView(view);
    });
  });

  // Default: This month
  var defaultBtn = document.querySelector("[data-chart-view=\"month\"]");
  if (defaultBtn) defaultBtn.classList.add("active");
  setChartView("month");
})();
