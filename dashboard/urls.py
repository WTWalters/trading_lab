# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Landing Page
    path('', views.landing_page, name='landing_page'),
    
    # Chart URLs (Story 5)
    path('chart/<str:ticker>/', views.chart_view, name='chart_view'),
    path('chart/', views.chart_view, name='chart_view_default'),

    # Backtest URL (Story 7)
    path('backtest/', views.backtest_view, name='backtest_view'),

    # Trade Log URLs (Story 10)
    path('tradelog/', views.trade_log_list_view, name='trade_log_list'),
    path('tradelog/new/', views.trade_log_create_view, name='trade_log_create'),
    path('tradelog/<int:pk>/', views.trade_log_detail_view, name='trade_log_detail'),
    path('tradelog/<int:pk>/update/', views.trade_log_update_view, name='trade_log_update'),
    path('tradelog/<int:pk>/delete/', views.trade_log_delete_view, name='trade_log_delete'),

    # Checklist Update URL (Story 13)
    path('tradelog/checklist/update/', views.update_checklist_item, name='update_checklist_item'),

    # Market Quote URL (Story 12)
    path('market-quote/', views.market_quote_view, name='market_quote'),

    # Educational Guidance URL (Story 15)
    path('education/query/', views.educational_guidance_view, name='education_query'),
]
