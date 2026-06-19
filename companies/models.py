from django.db import models

class DimCompany(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, null=True)
    company_logo = models.TextField(null=True)
    website = models.CharField(max_length=200, null=True)
    face_value = models.FloatField(null=True)
    book_value = models.FloatField(null=True)
    about_company = models.TextField(null=True)

    class Meta:
        db_table = 'dim_company'
        managed = False

class DimYear(models.Model):
    year_id = models.IntegerField(primary_key=True)
    year_label = models.CharField(max_length=20)
    fiscal_year = models.IntegerField(null=True)
    quarter = models.CharField(max_length=10, null=True)
    is_ttm = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True)

    class Meta:
        db_table = 'dim_year'
        managed = False

class FactProfitLoss(models.Model):
    symbol = models.ForeignKey(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        related_name='profit_loss'
    )
    year_id = models.ForeignKey(
        DimYear,
        on_delete=models.CASCADE,
        db_column='year_id',
        null=True,
        related_name='profit_loss'
    )
    sales = models.FloatField(null=True)
    expenses = models.FloatField(null=True)
    operating_profit = models.FloatField(null=True)
    opm_percentage = models.FloatField(null=True)
    net_profit = models.FloatField(null=True)
    eps = models.FloatField(null=True)
    dividend_payout = models.FloatField(null=True)
    interest_coverage = models.FloatField(null=True)
    net_profit_margin_pct = models.FloatField(null=True)
    expense_ratio_pct = models.FloatField(null=True)

    class Meta:
        db_table = 'fact_profit_loss'
        managed = False

class FactBalanceSheet(models.Model):
    symbol = models.ForeignKey(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        related_name='balance_sheet'
    )
    year_id = models.ForeignKey(
        DimYear,
        on_delete=models.CASCADE,
        db_column='year_id',
        null=True,
        related_name='balance_sheet'
    )
    equity_capital = models.FloatField(null=True)
    reserves = models.FloatField(null=True)
    borrowings = models.FloatField(null=True)
    fixed_assets = models.FloatField(null=True)
    total_assets = models.FloatField(null=True)
    debt_to_equity = models.FloatField(null=True)
    equity_ratio = models.FloatField(null=True)

    class Meta:
        db_table = 'fact_balance_sheet'
        managed = False

class FactCashFlow(models.Model):
    symbol = models.ForeignKey(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        related_name='cash_flow'
    )
    year_id = models.ForeignKey(
        DimYear,
        on_delete=models.CASCADE,
        db_column='year_id',
        null=True,
        related_name='cash_flow'
    )
    operating_activity = models.FloatField(null=True)
    investing_activity = models.FloatField(null=True)
    financing_activity = models.FloatField(null=True)
    net_cash_flow = models.FloatField(null=True)
    free_cash_flow = models.FloatField(null=True)
    cash_conversion_ratio = models.FloatField(null=True)

    class Meta:
        db_table = 'fact_cash_flow'
        managed = False

class FactMLScores(models.Model):
    symbol = models.OneToOneField(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        primary_key=True,
        related_name='ml_scores'
    )
    overall_score = models.FloatField(null=True)
    health_label = models.CharField(max_length=20, null=True)
    profitability_score = models.FloatField(null=True)
    growth_score = models.FloatField(null=True)
    leverage_score = models.FloatField(null=True)
    cashflow_score = models.FloatField(null=True)
    dividend_score = models.FloatField(null=True)
    trend_score = models.FloatField(null=True)

    class Meta:
        db_table = 'fact_ml_scores'
        managed = False

class FactProsCons(models.Model):
    symbol = models.OneToOneField(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        primary_key=True,
        related_name='pros_cons'
    )
    pros = models.TextField(null=True)
    cons = models.TextField(null=True)

    class Meta:
        db_table = 'fact_pros_cons'
        managed = False

class FactAnalysis(models.Model):
    symbol = models.OneToOneField(
        DimCompany,
        on_delete=models.CASCADE,
        db_column='symbol',
        primary_key=True,
        related_name='analysis'
    )
    compounded_sales_growth = models.FloatField(null=True)
    compounded_profit_growth = models.FloatField(null=True)
    stock_price_cagr = models.FloatField(null=True)
    roe = models.FloatField(null=True)

    class Meta:
        db_table = 'fact_analysis'
        managed = False