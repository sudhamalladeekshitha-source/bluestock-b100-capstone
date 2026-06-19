from django.shortcuts import render, get_object_or_404
from .models import (DimCompany, FactProfitLoss, FactMLScores,
                     FactBalanceSheet, FactCashFlow, FactProsCons)
from django.db.models import Avg, Sum, Count

def home(request):
    total = DimCompany.objects.count()
    sectors = DimCompany.objects.values('sector').annotate(
        count=Count('symbol')).order_by('-count')
    top_companies = FactMLScores.objects.select_related(
        'symbol').order_by('-overall_score')[:10]
    avg_score = FactMLScores.objects.aggregate(
        avg=Avg('overall_score'))['avg']
    return render(request, 'home.html', {
        'total_companies': total,
        'sectors': sectors,
        'top_companies': top_companies,
        'avg_score': round(avg_score or 0, 2)
    })

def company_list(request):
    companies = DimCompany.objects.all()
    sector = request.GET.get('sector')
    search = request.GET.get('search')
    if sector:
        companies = companies.filter(sector=sector)
    if search:
        companies = companies.filter(
            company_name__icontains=search)
    sectors = DimCompany.objects.values_list(
        'sector', flat=True).distinct()
    return render(request, 'companies/list.html', {
        'companies': companies,
        'sectors': sectors,
        'selected_sector': sector
    })

def company_detail(request, symbol):
    company = get_object_or_404(DimCompany, symbol=symbol)
    profit_loss = FactProfitLoss.objects.filter(
        symbol=symbol).order_by('year_id')
    balance_sheet = FactBalanceSheet.objects.filter(
        symbol=symbol).order_by('year_id')
    cash_flow = FactCashFlow.objects.filter(
        symbol=symbol).order_by('year_id')
    ml_scores = FactMLScores.objects.filter(symbol=symbol).first()
    pros_cons = FactProsCons.objects.filter(symbol=symbol).first()
    return render(request, 'companies/detail.html', {
        'company': company,
        'profit_loss': profit_loss,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
        'ml_scores': ml_scores,
        'pros_cons': pros_cons
    })

def sector_view(request):
    sectors = DimCompany.objects.values('sector').annotate(
        company_count=Count('symbol'),
        avg_opm=Avg('factprofitloss__opm_percentage'),
        total_revenue=Sum('factprofitloss__sales'),
        avg_health=Avg('factmlscores__overall_score')
    ).order_by('-total_revenue')
    return render(request, 'sectors.html', {
        'sectors': sectors
    })