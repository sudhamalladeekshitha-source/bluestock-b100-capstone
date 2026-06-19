from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count
from companies.models import (DimCompany, FactProfitLoss,
    FactBalanceSheet, FactCashFlow, FactMLScores,
    FactProsCons, FactAnalysis)
from companies.serializers import (CompanySerializer,
    ProfitLossSerializer, BalanceSheetSerializer,
    CashFlowSerializer, MLScoresSerializer,
    ProsConsSerializer, AnalysisSerializer)

class CompanyListView(generics.ListAPIView):
    queryset = DimCompany.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name', 'symbol', 'sector']

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = DimCompany.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'symbol'

class ProfitLossListView(generics.ListAPIView):
    serializer_class = ProfitLossSerializer
    def get_queryset(self):
        queryset = FactProfitLoss.objects.all()
        symbol = self.request.query_params.get('symbol')
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        return queryset

class BalanceSheetListView(generics.ListAPIView):
    serializer_class = BalanceSheetSerializer
    def get_queryset(self):
        queryset = FactBalanceSheet.objects.all()
        symbol = self.request.query_params.get('symbol')
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        return queryset

class CashFlowListView(generics.ListAPIView):
    serializer_class = CashFlowSerializer
    def get_queryset(self):
        queryset = FactCashFlow.objects.all()
        symbol = self.request.query_params.get('symbol')
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        return queryset

class MLScoresListView(generics.ListAPIView):
    serializer_class = MLScoresSerializer
    def get_queryset(self):
        queryset = FactMLScores.objects.all()
        symbol = self.request.query_params.get('symbol')
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        return queryset

@api_view(['GET'])
def market_overview(request):
    total = DimCompany.objects.count()
    avg_health = FactMLScores.objects.aggregate(
        avg=Avg('overall_score'))['avg']
    excellent = FactMLScores.objects.filter(
        health_label='EXCELLENT').count()
    poor = FactMLScores.objects.filter(
        health_label='POOR').count()
    sectors = DimCompany.objects.values(
        'sector').annotate(count=Count('symbol'))
    return Response({
        'total_companies': total,
        'avg_health_score': round(avg_health or 0, 2),
        'excellent_companies': excellent,
        'poor_companies': poor,
        'sectors': list(sectors)
    })

@api_view(['GET'])
def sector_analysis(request):
    sectors = DimCompany.objects.values('sector').annotate(
        company_count=Count('symbol'),
        avg_opm=Avg('factprofitloss__opm_percentage'),
        total_revenue=Sum('factprofitloss__sales'),
        avg_health=Avg('factmlscores__overall_score')
    ).order_by('-total_revenue')
    return Response(list(sectors))

@api_view(['GET'])
def top_companies(request):
    limit = int(request.query_params.get('limit', 10))
    companies = FactProfitLoss.objects.values(
        'symbol',
        'symbol__company_name',
        'symbol__sector'
    ).annotate(
        total_sales=Sum('sales')
    ).order_by('-total_sales')[:limit]
    return Response(list(companies))

@api_view(['GET'])
def company_health(request, symbol):
    try:
        company = DimCompany.objects.get(symbol=symbol)
        scores = FactMLScores.objects.filter(
            symbol=symbol).first()
        return Response({
            'company': CompanySerializer(company).data,
            'health_score': scores.overall_score if scores else None,
            'health_label': scores.health_label if scores else None,
        })
    except DimCompany.DoesNotExist:
        return Response(
            {'error': 'Company not found'}, status=404)