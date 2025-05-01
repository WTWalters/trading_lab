# dashboard/tests/test_models.py
import pytest
from decimal import Decimal
from django.utils import timezone
from django.db import IntegrityError # To test constraints if needed later
import pytz # For timezone

# Import the models to be tested
from dashboard.models import OHLCVData, TradeLog # Add TradeLog import

# Mark tests to use the database
pytestmark = pytest.mark.django_db

# --- Keep existing OHLCVData tests ---
def test_create_ohlcv_data_instance():
    """Test creating and saving an instance of the OHLCVData model."""
    now = timezone.now().replace(microsecond=0, tzinfo=pytz.UTC) # Ensure UTC

    # Create an instance
    ohlcv = OHLCVData.objects.create(
        timestamp=now,
        ticker="TEST",
        open=Decimal("100.50"),
        high=Decimal("102.75"),
        low=Decimal("99.80"),
        close=Decimal("101.25"),
        volume=1500000
    )

    # Retrieve it from the database
    # Use get with pk=ohlcv.pk for reliability if default id is used
    saved_ohlcv = OHLCVData.objects.get(pk=ohlcv.pk)

    # Assertions
    assert saved_ohlcv.ticker == "TEST"
    # Compare timestamps after ensuring both are UTC
    assert saved_ohlcv.timestamp == now.astimezone(pytz.UTC)
    assert saved_ohlcv.open == Decimal("100.50")
    assert saved_ohlcv.high == Decimal("102.75")
    assert saved_ohlcv.low == Decimal("99.80")
    assert saved_ohlcv.close == Decimal("101.25")
    assert saved_ohlcv.volume == 1500000

    # Test the __str__ method
    now_local_str = timezone.localtime(now).strftime('%Y-%m-%d %H:%M:%S %Z')
    assert str(saved_ohlcv) == f"TEST @ {now_local_str}"

# --- Add New Test Class for TradeLog ---
class TestTradeLogModel:
    """ Test cases for the TradeLog model. """

    def test_create_trade_log_required_fields(self):
        """ Test creating a TradeLog instance with only required fields. """
        entry_ts = timezone.now().replace(tzinfo=pytz.UTC)
        trade = TradeLog.objects.create(
            ticker="TRDLOG",
            strategy="Test Strategy",
            entry_date=entry_ts,
            entry_price=Decimal("200.00"),
            initial_stop_loss=Decimal("195.00"),
            position_size=Decimal("50.0"),
            user_risk_percent=Decimal("1.0"),
            account_capital_at_trade=Decimal("50000.00"),
            rationale="Test entry rationale."
        )
        assert trade.pk is not None # Check it was saved
        assert trade.ticker == "TRDLOG"
        assert trade.strategy == "Test Strategy"
        assert trade.entry_date == entry_ts
        assert trade.pnl is None # Optional field should be None
        assert trade.exit_date is None
        assert trade.rationale == "Test entry rationale."
        assert str(trade) == f"TRDLOG trade on {entry_ts.strftime('%Y-%m-%d')}"

    def test_create_trade_log_all_fields(self):
        """ Test creating a TradeLog instance with all fields populated. """
        entry_ts = timezone.now().replace(tzinfo=pytz.UTC)
        exit_ts = entry_ts + timezone.timedelta(days=5)
        trade = TradeLog.objects.create(
            ticker="FULL",
            strategy="Full Test",
            entry_date=entry_ts,
            exit_date=exit_ts,
            entry_price=Decimal("50.0"),
            exit_price=Decimal("55.0"),
            initial_stop_loss=Decimal("48.0"),
            planned_target=Decimal("60.0"),
            position_size=Decimal("100"),
            user_risk_percent=Decimal("0.5"),
            account_capital_at_trade=Decimal("20000.00"),
            rationale="All fields rationale.",
            emotion_pre="Excited",
            emotion_during="Calm",
            emotion_post="Satisfied",
            mistakes="None noted",
            lessons="Stick to plan",
            # Calculated fields can be set manually for testing if needed
            pnl=Decimal("500.00"), # (55-50)*100
            planned_rr_ratio=Decimal("5.0"), # (60-50)/(50-48) = 10/2
            suggested_position_size=Decimal("50.0") # (20000*0.005) / (50-48) = 100 / 2
        )
        assert trade.exit_date == exit_ts
        assert trade.exit_price == Decimal("55.0")
        assert trade.planned_target == Decimal("60.0")
        assert trade.emotion_pre == "Excited"
        assert trade.pnl == Decimal("500.00")
        assert trade.planned_rr_ratio == Decimal("5.0")
        assert trade.suggested_position_size == Decimal("50.0")

    def test_trade_log_ordering(self):
        """ Test the default ordering of TradeLog entries. """
        now = timezone.now().replace(tzinfo=pytz.UTC)
        t1 = TradeLog.objects.create(ticker="T1", strategy="S", entry_date=now - timezone.timedelta(days=2), entry_price=1, initial_stop_loss=1, position_size=1, user_risk_percent=1, account_capital_at_trade=1, rationale="R")
        t2 = TradeLog.objects.create(ticker="T2", strategy="S", entry_date=now, entry_price=1, initial_stop_loss=1, position_size=1, user_risk_percent=1, account_capital_at_trade=1, rationale="R")
        t3 = TradeLog.objects.create(ticker="T3", strategy="S", entry_date=now - timezone.timedelta(days=1), entry_price=1, initial_stop_loss=1, position_size=1, user_risk_percent=1, account_capital_at_trade=1, rationale="R")

        logs = list(TradeLog.objects.all()) # Uses default ordering ['-entry_date']
        assert logs[0] == t2 # Newest first
        assert logs[1] == t3
        assert logs[2] == t1
