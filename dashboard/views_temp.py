# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
from core.risk_calculator import calculate_rr_ratio, calculate_position_size
from django.contrib import messages
from .models import OHLCVData, TradeLog, TradeChecklistStatus, CLASSIC_BREAKOUT_CHECKLIST
from .forms import TradeLogForm
from core.educational_guidance import get_educational_context
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from core.backtester import run_backtest, get_available_date_range
from core.strategies import ClassicBreakoutStrategy
from core.market_data import get_latest_quote, is_tradable

def landing_page(request):
    """
    Landing page for the Trading Lab application.
    Provides an overview and links to various features.
    """
    return render(request, 'dashboard/landing_page.html')

# We'll import the rest of the views from the original file
from dashboard.views_original import *
