from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.CompanyListView.as_view(),
         name='company-list'),
    path('companies/<str:symbol>/',
         views.CompanyDetailView.as_view(),
         name='company-detail'),
    path('profit-loss/', views.ProfitLossListView.as_view(),
         name='profit-loss'),
    path('balance-sheet/', views.BalanceSheetListView.as_view(),
         name='balance-sheet'),
    path('cash-flow/', views.CashFlowListView.as_view(),
         name='cash-flow'),
    path('ml-scores/', views.MLScoresListView.as_view(),
         name='ml-scores'),
    path('market-overview/', views.market_overview,
         name='market-overview'),
    path('sector-analysis/', views.sector_analysis,
         name='sector-analysis'),
    path('top-companies/', views.top_companies,
         name='top-companies'),
    path('company-health/<str:symbol>/',
         views.company_health,
         name='company-health'),
]