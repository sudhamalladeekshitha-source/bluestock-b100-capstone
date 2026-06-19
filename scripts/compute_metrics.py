import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load Data
nav_df = pd.read_csv('nav_data.csv', parse_dates=['Date']).set_index('Date')
fund_scorecard = pd.read_csv('fund_scorecard.csv').set_index('Fund')
expense_df = pd.read_csv('expense_ratio.csv')
daily_returns = nav_df.pct_change().dropna()
fund_names = nav_df.columns.tolist()
print(f"✅ Loaded {len(fund_names)} funds")

# Task 1 - VaR & CVaR
var_records = []
for fund in fund_names:
    r = daily_returns[fund]
    var_95 = np.percentile(r, 5)
    cvar_95 = r[r <= var_95].mean()
    var_records.append({
        'Fund': fund,
        'VaR_95_%': round(var_95*100, 4),
        'CVaR_95_%': round(cvar_95*100, 4)
    })
var_df = pd.DataFrame(var_records).set_index('Fund')
var_df.to_csv('var_cvar_report.csv')
print("✅ Task 1 Done - var_cvar_report.csv saved")

# Task 2 - Rolling Sharpe
RF = 0.065/252
top5 = fund_names[:5]
fig, ax = plt.subplots(figsize=(14,6))
colors = ['#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6']
for i, fund in enumerate(top5):
    r = daily_returns[fund]
    rolling_sharpe = (r.rolling(90).mean() - RF) / r.rolling(90).std() * np.sqrt(252)
    ax.plot(rolling_sharpe.index, rolling_sharpe, label=fund[:25], color=colors[i], linewidth=1.5)
ax.set_title('Rolling 90-Day Sharpe Ratio — Top 5 Funds', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.legend(fontsize=8)
ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.tight_layout()
plt.savefig('rolling_sharpe_chart.png', dpi=150, bbox_inches='tight')
print("✅ Task 2 Done - rolling_sharpe_chart.png saved")

# Task 3 - Investor Cohort
inv_df = pd.read_csv('investor_data.csv', parse_dates=['transaction_date'])
cohort = inv_df.groupby(['first_year','investor_id']).agg(
    avg_sip=('sip_amount','mean'),
    total_invested=('sip_amount','sum'),
    top_fund=('fund', lambda x: x.mode()[0])
).reset_index()
cohort_summary = cohort.groupby('first_year').agg(
    avg_sip_amount=('avg_sip','mean'),
    total_invested=('total_invested','sum'),
    investors=('investor_id','count')
).round(2)
print("✅ Task 3 Done - Cohort Analysis:")
print(cohort_summary)

# Task 4 - SIP Continuity
sip_df = inv_df[inv_df['transaction_type']=='SIP'].copy()
sip_df = sip_df.sort_values(['investor_id','transaction_date'])
continuity = []
for inv_id, group in sip_df.groupby('investor_id'):
    if len(group) >= 6:
        gaps = group['transaction_date'].diff().dt.days.dropna()
        avg_gap = gaps.mean()
        status = 'At-Risk' if avg_gap > 35 else 'Regular'
        continuity.append({
            'investor_id': inv_id,
            'avg_gap_days': round(avg_gap, 1),
            'num_sips': len(group),
            'status': status
        })
cont_df = pd.DataFrame(continuity)
print(f"✅ Task 4 Done - At-Risk: {(cont_df['status']=='At-Risk').sum()} | Regular: {(cont_df['status']=='Regular').sum()}")

# Task 5 - Fund Recommender
var_df['risk_grade'] = pd.cut(
    var_df['VaR_95_%'],
    bins=[-999, -1.5, -1.0, 0],
    labels=['High','Moderate','Low']
)
def recommend_funds(risk_appetite):
    filtered = var_df[var_df['risk_grade']==risk_appetite].copy()
    filtered['Sharpe'] = fund_scorecard['Sharpe']
    top3 = filtered.nlargest(3,'Sharpe')[['VaR_95_%','CVaR_95_%','Sharpe','risk_grade']]
    print(f"\n🎯 Top 3 Funds for {risk_appetite} Risk:")
    print(top3.to_string())
recommend_funds('Low')
recommend_funds('Moderate')
recommend_funds('High')
print("✅ Task 5 Done - Recommender")

# Task 6 - Sector HHI
sector_df = pd.read_csv('sector_weights.csv')
hhi_records = []
for fund, group in sector_df.groupby('Fund'):
    hhi = (group['Weight']**2).sum()
    hhi_records.append({
        'Fund': fund,
        'HHI': round(hhi, 4),
        'Concentration': 'High' if hhi > 0.2 else ('Medium' if hhi > 0.1 else 'Low')
    })
hhi_df = pd.DataFrame(hhi_records).set_index('Fund')
print("✅ Task 6 Done - HHI Analysis:")
print(hhi_df.sort_values('HHI', ascending=False).head(5))

print("\n✅ ALL TASKS COMPLETE!")
print("Files saved:")
print("  - var_cvar_report.csv")
print("  - rolling_sharpe_chart.png")