
import {
  ShieldAlert, LayoutDashboard, CreditCard, Bell,
  ChartNoAxesCombined, Settings, Search, ArrowUpRight,
  ArrowDownRight, ShieldCheck, Activity, Menu
} from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  Tooltip, CartesianGrid, PieChart, Pie, Cell
} from "recharts";
import "./App.css";

const activity = [
  { day: "Mon", transactions: 120, fraud: 12 },
  { day: "Tue", transactions: 180, fraud: 18 },
  { day: "Wed", transactions: 150, fraud: 10 },
  { day: "Thu", transactions: 240, fraud: 24 },
  { day: "Fri", transactions: 200, fraud: 15 },
  { day: "Sat", transactions: 290, fraud: 30 },
  { day: "Sun", transactions: 260, fraud: 20 },
];

const transactions = [
  { id: "TXN-10042", customer: "Customer #104", amount: "$2,450.00", time: "10:42 AM", risk: "High", status: "Fraud" },
  { id: "TXN-10041", customer: "Customer #087", amount: "$125.50", time: "10:38 AM", risk: "Low", status: "Legitimate" },
  { id: "TXN-10040", customer: "Customer #221", amount: "$890.00", time: "10:31 AM", risk: "Medium", status: "Review" },
  { id: "TXN-10039", customer: "Customer #056", amount: "$3,200.00", time: "10:25 AM", risk: "High", status: "Fraud" },
  { id: "TXN-10038", customer: "Customer #193", amount: "$64.99", time: "10:19 AM", risk: "Low", status: "Legitimate" },
];

const distribution = [
  { name: "Legitimate", value: 82, color: "#22c55e" },
  { name: "Review", value: 12, color: "#f59e0b" },
  { name: "Fraud", value: 6, color: "#f43f5e" },
];

function Sidebar() {
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
        <a className="nav-item" href="#alerts"><Bell size={18} /> Fraud Alerts <span className="nav-count">4</span></a>
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

function StatCard({ title, value, change, positive, icon: Icon, color, note }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{title}</span>
        <div className={`stat-icon ${color}`}><Icon size={19} /></div>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-footer">
        <span className={positive ? "change positive" : "change negative"}>
          {positive ? <ArrowUpRight size={15} /> : <ArrowDownRight size={15} />}
          {change}
        </span>
        <span className="muted">{note}</span>
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <main className="main-content" id="dashboard">
      <header className="topbar">
        <div className="mobile-brand"><Menu size={22} /> FraudGuard</div>
        <div className="breadcrumb">Workspace <span>/</span> <strong>Dashboard</strong></div>
        <div className="top-actions">
          <span className="live-badge"><span className="online-dot" /> LIVE SYSTEM</span>
          <button className="icon-button" aria-label="Notifications"><Bell size={19} /></button>
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
          <div className="date-label"><Activity size={16} /> Demo data · Last 7 days</div>
        </section>

        <section className="stats-grid">
          <StatCard title="Total Transactions" value="24,586" change="12.8%" positive icon={CreditCard} color="blue" note="vs previous period" />
          <StatCard title="Fraud Detected" value="184" change="8.2%" positive={false} icon={ShieldAlert} color="red" note="vs previous period" />
          <StatCard title="Fraud Rate" value="0.75%" change="0.3%" positive icon={ChartNoAxesCombined} color="amber" note="vs previous period" />
          <StatCard title="Transactions Cleared" value="24,402" change="99.25%" positive icon={ShieldCheck} color="green" note="of total transactions" />
        </section>

        <section className="charts-grid" id="analytics">
          <div className="panel chart-panel">
            <div className="panel-heading">
              <div><h2>Transaction Activity</h2><p>Transaction volume and detected fraud</p></div>
              <span className="period-pill">Last 7 days⌄</span>
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
              <div className="donut-center"><strong>100%</strong><span>Analyzed</span></div>
            </div>
            <div className="distribution-legend">
              {distribution.map(item => (
                <div key={item.name} className="distribution-row">
                  <span><i style={{ background: item.color }} />{item.name}</span>
                  <strong>{item.value}%</strong>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bottom-grid">
          <div className="panel table-panel" id="transactions">
            <div className="panel-heading">
              <div><h2>Recent Transactions</h2><p>Latest processed card transactions</p></div>
              <a className="text-link" href="#transactions">View all <ArrowUpRight size={15} /></a>
            </div>
            <div className="table-search"><Search size={16} /><input placeholder="Search transaction ID..." /></div>
            <div className="table-scroll">
              <table>
                <thead><tr><th>TRANSACTION</th><th>AMOUNT</th><th>RISK</th><th>STATUS</th></tr></thead>
                <tbody>
                  {transactions.map(tx => (
                    <tr key={tx.id}>
                      <td><strong>{tx.id}</strong><small>{tx.time} · {tx.customer}</small></td>
                      <td>{tx.amount}</td>
                      <td><span className={`risk risk-${tx.risk.toLowerCase()}`}>{tx.risk}</span></td>
                      <td><span className={`status status-${tx.status.toLowerCase()}`}>{tx.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="panel alerts-panel" id="alerts">
            <div className="panel-heading">
              <div><h2>Priority Alerts</h2><p>Transactions requiring attention</p></div>
              <span className="alert-number">2 NEW</span>
            </div>
            <div className="alert-item">
              <div className="alert-symbol"><ShieldAlert size={18} /></div>
              <div className="alert-copy"><strong>Unusual transaction amount</strong><p>TXN-10042 · $2,450.00</p><span>2 minutes ago</span></div>
              <span className="severity">HIGH</span>
            </div>
            <div className="alert-item">
              <div className="alert-symbol"><ShieldAlert size={18} /></div>
              <div className="alert-copy"><strong>Suspicious spending pattern</strong><p>TXN-10039 · $3,200.00</p><span>8 minutes ago</span></div>
              <span className="severity">HIGH</span>
            </div>
            <div className="alert-footer"><ShieldCheck size={16} /> Monitoring system is active</div>
          </div>
        </section>
        <footer className="footer">FraudGuard Intelligence <span>AI-powered transaction monitoring</span></footer>
      </div>
    </main>
  );
}

export default function App() {
  return <div className="app-shell"><Sidebar /><Dashboard /></div>;
}
