import pandas as pd

var_df = pd.read_csv('var_cvar_report.csv').set_index('Fund')
scorecard = pd.read_csv('fund_scorecard.csv').set_index('Fund')

var_df['risk_grade'] = pd.cut(
    var_df['VaR_95_%'],
    bins=[-999, -1.5, -1.0, 0],
    labels=['High','Moderate','Low']
)

def recommend_funds(risk_appetite):
    filtered = var_df[var_df['risk_grade']==risk_appetite].copy()
    filtered['Sharpe'] = scorecard['Sharpe']
    top3 = filtered.nlargest(3,'Sharpe')[['VaR_95_%','CVaR_95_%','Sharpe','risk_grade']]
    print(f"\n🎯 Top 3 Funds for {risk_appetite} Risk:")
    print(top3.to_string())

risk = input("Enter risk appetite (Low/Moderate/High): ")
recommend_funds(risk)