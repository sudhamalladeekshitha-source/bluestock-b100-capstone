"""
run_pipeline.py
===============
Master execution script for Bluestock Fintech Mutual Fund Analytics.
Runs all tasks in sequence and generates all deliverables.

Usage:
    python run_pipeline.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def load_data():
    """Load all required CSV files."""
    nav_df = pd.read_csv('nav_data.csv', parse_dates=['Date']).set_index('Date')
    nifty100 = pd.read_csv('nifty100.csv', parse_dates=['Date']).set_index('Date')
    nifty50 = pd.read_csv('nifty50.csv', parse_dates=['Date']).set_index('Date')
    expense_df = pd.read_csv('expense_ratio.csv')
    print(f"✅ Data loaded: {nav_df.shape[1]} funds, {len(nav_df)} days")
    return nav_df, nifty100, nifty50, expense_df


def compute_daily_returns(nav_df):
    """Compute daily returns for all funds."""
    daily_returns = nav_df.pct_change().dropna()
    print(f"✅ Daily returns computed: {daily_returns.shape}")
    return daily_returns


def compute_cagr(nav_series, years):
    """Compute CAGR for given number of years."""
    end_date = nav_series.index[-1]
    start_date = end_date - pd.DateOffset(years=years)
    nav_slice = nav_series[nav_series.index >= start_date]
    if len(nav_slice) < 2:
        return np.nan
    return (nav_slice.iloc[-1] / nav_slice.iloc[0]) ** (1/years) - 1


def compute_sharpe(returns, rf_daily=0.065/252):
    """Compute annualized Sharpe ratio."""
    return (returns.mean() - rf_daily) / returns.std() * np.sqrt(252)


def compute_var_cvar(returns):
    """Compute VaR (95%) and CVaR."""
    var_95 = np.percentile(returns, 5)
    cvar_95 = returns[returns <= var_95].mean()
    return var_95, cvar_95


def run_performance_analytics(nav_df, nifty100, expense_df, daily_returns):
    """Run Task 4: Performance Analytics."""
    print("\n--- Task 4: Performance Analytics ---")
    fund_names = nav_df.columns.tolist()
    RF = 0.065 / 252

    records = []
    for fund in fund_names:
        r = daily_returns[fund]
        var95, cvar95 = compute_var_cvar(r)
        slope, intercept, r_val, _, _ = stats.linregress(
            nifty100['Close'].pct_change().dropna().loc[r.index],
            r
        )
        records.append({
            'Fund': fund,
            'CAGR_3yr': round(compute_cagr(nav_df[fund], 3)*100, 2),
            'Sharpe': round(compute_sharpe(r), 4),
            'Alpha': round(intercept * 252 * 100, 4),
            'Beta': round(slope, 4),
            'VaR_95_%': round(var95*100, 4),
            'CVaR_95_%': round(cvar95*100, 4)
        })

    results_df = pd.DataFrame(records).set_index('Fund')
    results_df.to_csv('var_cvar_report.csv')
    print(f"✅ Performance analytics complete. var_cvar_report.csv saved.")
    return results_df


def run_advanced_analytics(nav_df, daily_returns):
    """Run Task 5: Advanced Analytics."""
    print("\n--- Task 5: Advanced Analytics ---")
    fund_names = nav_df.columns.tolist()
    RF = 0.065 / 252

    # Rolling Sharpe chart
    top5 = fund_names[:5]
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ['#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6']
    for i, fund in enumerate(top5):
        r = daily_returns[fund]
        rs = (r.rolling(90).mean() - RF) / r.rolling(90).std() * np.sqrt(252)
        ax.plot(rs.index, rs, label=fund[:25], color=colors[i], linewidth=1.5)
    ax.set_title('Rolling 90-Day Sharpe Ratio', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sharpe Ratio')
    ax.legend(fontsize=8)
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.savefig('rolling_sharpe_chart.png', dpi=150, bbox_inches='tight')
    print("✅ rolling_sharpe_chart.png saved")


def main():
    """Main pipeline execution."""
    print("=" * 50)
    print("🚀 BLUESTOCK MF ANALYTICS PIPELINE")
    print("=" * 50)

    nav_df, nifty100, nifty50, expense_df = load_data()
    daily_returns = compute_daily_returns(nav_df)
    results_df = run_performance_analytics(nav_df, nifty100, expense_df, daily_returns)
    run_advanced_analytics(nav_df, daily_returns)

    print("\n" + "=" * 50)
    print("✅ PIPELINE COMPLETE! All files generated.")
    print("=" * 50)


if __name__ == "__main__":
    main()
