import { useEffect, useMemo, useState } from "react";
import {
  ShieldAlert, LayoutDashboard, CreditCard, Bell,
  ChartNoAxesCombined, Settings, Search, ArrowUpRight,
  ArrowDownRight, ShieldCheck, Activity, Menu,
} from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  Tooltip, CartesianGrid, PieChart, Pie, Cell,
} from "recharts";
import {
  getHealth,
  getTransactions,
  getAlerts,
  getModelPerformance,
} from "./services/api";
import "./App.css";

const COLORS = {
  Legitimate: "#22c55e",
  Review: "#f59e0b",
  Fraud: "#f43f5e",
};

function Sidebar({ alertCount }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon"><ShieldAlert size={23} /></div>
        <div><strong>FraudGuard</strong><small>INTELLIGENCE PLATFORM</small></div>
      </div>
      <div className="nav-label">WORKSPACE</div>
      <nav>
        <a className="nav-item active" href="#dashboard"><LayoutDashboard size={18} /> Dashboard</a>
        <a className="nav-item" href="#transactions"><CreditCard size={18} /> Transactions</a>
        <a className="nav-item" href="#alerts"><Bell size={18} /> Fraud Alerts <span className="nav-count">{alertCount}</span></a>
        <a className="nav-item" href="#analytics"><ChartNoAxesCombined size={18} /> Analytics</a>
      </nav>
      <div className="sidebar-bottom">
        <div className="system-status"><span className="online-dot" /> System operational</div>
        <a className="nav-item" href="#settings"><Settings size={18} /> Settings</a>
        <div className="profile">
          <div className="avatar">FA</div>
          <div><strong>Fraud Analyst</strong><small>Analyst account</small></div>
        </div>
      </div>
    </aside>
  );
}

function StatCard({ title, value, icon: Icon, color, note }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{title}</span>
        <div className={`stat-icon ${color}`}><Icon size={19} /></div>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-footer">
        <span className="muted">{note}</span>
      </div>
    </div>
  );
}

function formatAmount(amount) {
  const value = Number(amount);
  return Number.isFinite(value)
    ? new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(value)
    : "—";
}

function getStatus(tx) {
  if (tx.prediction === "Fraud") return "Fraud";
  if (tx.risk_level === "Medium") return "Review";
  return tx.prediction || "Unknown";
}

function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [health, setHealth] = useState("Checking");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    let active = true;

    async function loadDashboard() {
      try {
        const results = await Promise.allSettled([
          getHealth(),
          getTransactions(),
          getAlerts(),
          getModelPerformance(),
        ]);

        if (!active) return;

        const [healthResult, txResult, alertsResult, perfResult] = results;

        if (healthResult.status === "fulfilled") {
          setHealth(healthResult.value.database || "Connected");
        } else {
          setHealth("Unavailable");
        }

        if (txResult.status === "fulfilled") {
          setTransactions(txResult.value);
        }

        if (alertsResult.status === "fulfilled") {
          setAlerts(alertsResult.value);
        }

        if (perfResult.status === "fulfilled") {
          setPerformance(perfResult.value);
        }

        const failures = results.filter(
          (result) => result.status === "rejected"
        );

        if (failures.length === results.length) {
          setError("Could not connect to the backend. Check that FastAPI is running.");
        } else if (failures.length > 0) {
          setError("Some dashboard data could not be loaded. Check the backend endpoints.");
        } else {
          setError("");
        }
      } catch {
        if (active) setError("Unable to load dashboard data.");
      } finally {
        if (active) setLoading(false);
      }
    }

    loadDashboard();

    return () => {
      active = false;
    };
  }, []);

  const filteredTransactions = useMemo(() => {
    const term = search.trim().toLowerCase();
    return transactions.filter((tx) =>
      String(tx.transaction_id ?? "")
        .toLowerCase()
        .includes(term)
    );
  }, [transactions, search]);

  const fraudCount = transactions.filter(
    (tx) => tx.prediction === "Fraud"
  ).length;

  const legitimateCount = transactions.filter(
    (tx) => tx.prediction === "Legitimate"
  ).length;

  const mediumCount = transactions.filter(
    (tx) => tx.risk_level === "Medium"
  ).length;

  const total = transactions.length;
  const fraudRate = total ? ((fraudCount / total) * 100).toFixed(2) : "0.00";

  const distribution = [
    { name: "Legitimate", value: legitimateCount, color: COLORS.Legitimate },
    { name: "Review", value: mediumCount, color: COLORS.Review },
    { name: "Fraud", value: fraudCount, color: COLORS.Fraud },
  ].filter((item) => item.value > 0);

  const activity = useMemo(() => {
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const groups = new Map();

    for (const tx of transactions) {
      const date = tx.created_at ? new Date(tx.created_at) : null;
      if (!date || Number.isNaN(date.getTime())) continue;

      const key = date.toLocaleDateString();
      if (!groups.has(key)) {
        groups.set(key, {
          day: days[date.getDay()],
          transactions: 0,
          fraud: 0,
          timestamp: date.getTime(),
        });
      }

      const group = groups.get(key);
      group.transactions += 1;
      if (tx.prediction === "Fraud") group.fraud += 1;
    }

    return [...groups.values()]
      .sort((a, b) => a.timestamp - b.timestamp)
      .slice(-7);
  }, [transactions]);

  return (
    <main className="main-content" id="dashboard">
      <header className="topbar">
        <div className="mobile-brand"><Menu size={22} /> FraudGuard</div>
        <div className="breadcrumb">Workspace <span>/</span> <strong>Dashboard</strong></div>
        <div className="top-actions">
          <span className="live-badge">
            <span className="online-dot" /> {health.toUpperCase()}
          </span>
          <button className="icon-button" aria-label="Notifications">
            <Bell size={19} />
          </button>
          <div className="avatar">FA</div>
        </div>
      </header>

      <div className="page-content">
        <section className="page-heading">
          <div>
            <div className="eyebrow">OVERVIEW / MONITORING</div>
            <h1>Fraud Detection Dashboard</h1>
            <p>Monitor transactions, detect suspicious activity, and review fraud risks.</p>
          </div>
          <div className="date-label"><Activity size={16} /> Live database data</div>
        </section>

        {error && <p role="alert">{error}</p>}
        {loading && <p>Loading dashboard data…</p>}

        <section className="stats-grid">
          <StatCard title="Total Transactions" value={total.toLocaleString()} icon={CreditCard} color="blue" note="Stored transactions" />
          <StatCard title="Fraud Detected" value={fraudCount.toLocaleString()} icon={ShieldAlert} color="red" note="Predicted as fraud" />
          <StatCard title="Fraud Rate" value={`${fraudRate}%`} icon={ChartNoAxesCombined} color="amber" note="Of stored transactions" />
          <StatCard title="Transactions Cleared" value={legitimateCount.toLocaleString()} icon={ShieldCheck} color="green" note="Predicted legitimate" />
        </section>

        <section className="charts-grid" id="analytics">
          <div className="panel chart-panel">
            <div className="panel-heading">
              <div><h2>Transaction Activity</h2><p>Stored transaction volume and detected fraud</p></div>
              <span className="period-pill">Last 7 recorded days</span>
            </div>
            <div className="legend">
              <span><i className="legend-blue" /> Transactions</span>
              <span><i className="legend-red" /> Fraud detected</span>
            </div>
            <div className="chart-area">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={activity} margin={{ top: 12, right: 8, left: -18, bottom: 0 }}>
                  <defs>
                    <linearGradient id="transactionFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6288ff" stopOpacity={0.25} />
                      <stop offset="100%" stopColor="#6288ff" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#253047" strokeDasharray="4 4" vertical={false} />
                  <XAxis dataKey="day" tick={{ fill: "#8b98ad", fontSize: 12 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: "#8b98ad", fontSize: 12 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: "#151e30", border: "1px solid #303d53", borderRadius: 10 }} />
                  <Area type="monotone" dataKey="transactions" stroke="#6288ff" strokeWidth={2.5} fill="url(#transactionFill)" />
                  <Area type="monotone" dataKey="fraud" stroke="#fb7185" strokeWidth={2} fill="transparent" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="panel distribution-panel">
            <div className="panel-heading">
              <div><h2>Risk Distribution</h2><p>Transaction classification</p></div>
            </div>
            <div className="donut-wrap">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={distribution} dataKey="value" nameKey="name" innerRadius={67} outerRadius={91} paddingAngle={4} stroke="none">
                    {distribution.map((item) => <Cell key={item.name} fill={item.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#151e30", border: "1px solid #303d53", borderRadius: 10 }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="donut-center">
                <strong>{total ? "100%" : "0%"}</strong>
                <span>Analyzed</span>
              </div>
            </div>
            <div className="distribution-legend">
              {distribution.map((item) => (
                <div key={item.name} className="distribution-row">
                  <span><i style={{ background: item.color }} />{item.name}</span>
                  <strong>{total ? `${((item.value / total) * 100).toFixed(1)}%` : "0%"}</strong>
                </div>
              ))}
              {total === 0 && <p>No transaction data yet.</p>}
            </div>
          </div>
        </section>

        <section className="bottom-grid">
          <div className="panel table-panel" id="transactions">
            <div className="panel-heading">
              <div><h2>Recent Transactions</h2><p>Latest processed card transactions</p></div>
              <span className="text-link">{filteredTransactions.length} records</span>
            </div>
            <div className="table-search">
              <Search size={16} />
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search transaction ID..."
              />
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr><th>TRANSACTION</th><th>AMOUNT</th><th>RISK</th><th>STATUS</th></tr>
                </thead>
                <tbody>
                  {filteredTransactions.slice(0, 10).map((tx) => {
                    const risk = tx.risk_level || "Low";
                    const status = getStatus(tx);
                    return (
                      <tr key={`${tx._id || tx.transaction_id}`}>
                        <td>
                          <strong>{tx.transaction_id || "Unknown ID"}</strong>
                          <small>{tx.created_at ? new Date(tx.created_at).toLocaleString() : "Time unavailable"}</small>
                        </td>
                        <td>{formatAmount(tx.Amount)}</td>
                        <td><span className={`risk risk-${risk.toLowerCase()}`}>{risk}</span></td>
                        <td><span className={`status status-${status.toLowerCase()}`}>{status}</span></td>
                      </tr>
                    );
                  })}
                  {!loading && filteredTransactions.length === 0 && (
                    <tr><td colSpan="4">No matching transactions found.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="panel alerts-panel" id="alerts">
            <div className="panel-heading">
              <div><h2>Priority Alerts</h2><p>Transactions requiring attention</p></div>
              <span className="alert-number">{alerts.length} ALERTS</span>
            </div>
            {alerts.slice(0, 5).map((alert) => (
              <div className="alert-item" key={alert.alert_id}>
                <div className="alert-symbol"><ShieldAlert size={18} /></div>
                <div className="alert-copy">
                  <strong>{alert.prediction || "Suspicious transaction"}</strong>
                  <p>{alert.transaction_id} · {formatAmount(
                    transactions.find((tx) => tx.transaction_id === alert.transaction_id)?.Amount
                  )}</p>
                  <span>{alert.created_at ? new Date(alert.created_at).toLocaleString() : "Time unavailable"}</span>
                </div>
                <span className="severity">{alert.risk_level || "HIGH"}</span>
              </div>
            ))}
            {alerts.length === 0 && !loading && <p>No alerts found.</p>}
            <div className="alert-footer"><ShieldCheck size={16} /> Monitoring system is active</div>
          </div>
        </section>

        <section className="panel" style={{ marginTop: 20, padding: 20 }}>
          <h2>Model Performance</h2>
          {performance ? (
            <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
              {JSON.stringify(performance, null, 2)}
            </pre>
          ) : (
            <p>Model performance data unavailable.</p>
          )}
        </section>

        <footer className="footer">
          FraudGuard Intelligence <span>AI-powered transaction monitoring</span>
        </footer>
      </div>
    </main>
  );
}

export default function App() {
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    getAlerts()
      .then((items) => setAlertCount(items.length))
      .catch(() => setAlertCount(0));
  }, []);

  return (
    <div className="app-shell">
      <Sidebar alertCount={alertCount} />
      <Dashboard />
    </div>
  );
}
