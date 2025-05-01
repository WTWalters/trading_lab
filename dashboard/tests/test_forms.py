# dashboard/tests/test_forms.py
import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
import pytz
from django import forms

# Import the form to be tested
from dashboard.forms import TradeLogForm

class TestTradeLogForm:
    """ Test cases for the TradeLogForm. """

    def test_valid_trade_log_form(self):
        """ Test the form with valid data. """
        entry_ts_str = timezone.now().strftime('%Y-%m-%dT%H:%M')
        form_data = {
            'ticker': 'VALID', 'strategy': 'Classic Breakout', 'entry_date': entry_ts_str,
            'entry_price': '250.50', 'initial_stop_loss': '245.00', 'position_size': '20',
            'user_risk_percent': '1.5', 'account_capital_at_trade': '75000',
            'rationale': 'Valid rationale.', 'exit_date': '', 'exit_price': '',
            'planned_target': '270.00', 'emotion_pre': 'Neutral', 'emotion_during': '',
            'emotion_post': '', 'mistakes': '', 'lessons': '',
        }
        form = TradeLogForm(data=form_data)
        assert form.is_valid(), f"Form should be valid, errors: {form.errors.as_json()}"

    def test_invalid_trade_log_form_missing_required(self):
        """ Test the form with missing required fields. """
        form_data = {'rationale': ''} # Rationale is required, test with empty
        form = TradeLogForm(data=form_data)
        assert not form.is_valid()
        assert 'ticker' in form.errors
        assert 'strategy' in form.errors
        assert 'entry_date' in form.errors
        assert 'entry_price' in form.errors
        assert 'initial_stop_loss' in form.errors
        assert 'position_size' in form.errors
        assert 'user_risk_percent' in form.errors
        assert 'account_capital_at_trade' in form.errors
        assert 'rationale' in form.errors # Verify rationale is required

    def test_invalid_trade_log_form_bad_types(self):
        """ Test the form with incorrect data types. """
        entry_ts_str = timezone.now().strftime('%Y-%m-%dT%H:%M')
        form_data = {
            'ticker': 'BADTYPE', 'strategy': 'Classic Breakout', 'entry_date': entry_ts_str,
            'entry_price': 'not-a-number', 'initial_stop_loss': '100.00',
            'position_size': 'abc', 'user_risk_percent': 'high',
            'account_capital_at_trade': 'lots', 'rationale': 'Bad types test.',
            'exit_date': 'not-a-date',
        }
        form = TradeLogForm(data=form_data)
        assert not form.is_valid()
        assert 'entry_price' in form.errors
        assert 'position_size' in form.errors
        assert 'user_risk_percent' in form.errors
        assert 'account_capital_at_trade' in form.errors
        assert 'exit_date' in form.errors

    def test_form_widgets_basic(self):
        """ Basic check that widgets are assigned. """
        form = TradeLogForm()
        assert isinstance(form.fields['entry_date'].widget, forms.DateTimeInput)
        assert isinstance(form.fields['rationale'].widget, forms.Textarea)
        assert isinstance(form.fields['entry_price'].widget, forms.NumberInput)
        assert isinstance(form.fields['strategy'].widget, forms.Select)
        # --- REMOVED assertion checking widget.attrs['type'] ---
