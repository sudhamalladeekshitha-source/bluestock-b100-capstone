-- Bluestock MF Analytics Database Schema

CREATE TABLE IF NOT EXISTS nav_data (
    date DATE NOT NULL,
    fund_name TEXT NOT NULL,
    nav REAL NOT NULL,
    PRIMARY KEY (date, fund_name)
);

CREATE TABLE IF NOT EXISTS fund_scorecard (
    fund TEXT PRIMARY KEY,
    cagr_3yr REAL,
    sharpe REAL,
    alpha REAL,
    expense_ratio REAL,
    max_drawdown REAL,
    score REAL
);

CREATE TABLE IF NOT EXISTS alpha_beta (
    fund TEXT PRIMARY KEY,
    alpha_annualized REAL,
    beta REAL,
    r_squared REAL
);

CREATE TABLE IF NOT EXISTS var_cvar (
    fund TEXT PRIMARY KEY,
    var_95_pct REAL,
    cvar_95_pct REAL,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS investor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    first_year INTEGER,
    transaction_date DATE,
    sip_amount REAL,
    fund TEXT,
    transaction_type TEXT
);