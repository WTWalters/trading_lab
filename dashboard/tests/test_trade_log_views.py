# dashboard/tests/test_trade_log_views.py
import pytest
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import pytz

# Import models and forms
from dashboard.models import TradeLog
from dashboard.forms import TradeLogForm

@pytest.mark.django_db
class TestTradeLogViews:
    """ Tests for the TradeLog related views. """

    def setup_method(self):
        self.client = Client()
        self.list_url = reverse('dashboard:trade_log_list')
        self.create_url = reverse('dashboard:trade_log_create')
        # Create a sample log for update/detail/delete tests
        # Ensure timezone-aware datetime for entry_date
        self.entry_ts = timezone.make_aware(datetime(2025, 4, 26, 10, 0, 0), timezone.get_default_timezone()) # Example aware datetime

        self.trade_log = TradeLog.objects.create(
            ticker="TESTLOG", strategy="Strategy 1", entry_date=self.entry_ts,
            entry_price=Decimal("100.00"), initial_stop_loss=Decimal("95.00"),
            position_size=Decimal("10"), user_risk_percent=Decimal("1.0"),
            account_capital_at_trade=Decimal("10000.00"), rationale="Initial Log"
        )
        self.detail_url = reverse('dashboard:trade_log_detail', kwargs={'pk': self.trade_log.pk})
        self.update_url = reverse('dashboard:trade_log_update', kwargs={'pk': self.trade_log.pk})
        self.delete_url = reverse('dashboard:trade_log_delete', kwargs={'pk': self.trade_log.pk})

    # --- List View Tests ---
    def test_trade_log_list_view_get(self):
        """ Test GET request for the trade log list view. """
        response = self.client.get(self.list_url)
        assert response.status_code == 200
        assert 'trade_logs' in response.context
        # Convert entry_date from context to aware datetime if necessary for comparison
        log_in_context = response.context['trade_logs'].first()
        assert log_in_context is not None
        assert log_in_context.pk == self.trade_log.pk
        assert 'dashboard/trade_log_list.html' in [t.name for t in response.templates]

    # --- Create View Tests ---
    def test_trade_log_create_view_get(self):
        """ Test GET request for the trade log create view. """
        response = self.client.get(self.create_url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], TradeLogForm)
        assert 'dashboard/trade_log_form.html' in [t.name for t in response.templates]
        # Check initial data if needed
        assert response.context['form'].initial.get('strategy') == 'Classic Breakout'

    # REMOVED SKIP
    def test_trade_log_create_view_post_valid(self):
        """ Test POST request with valid data for creating a trade log. """
        # Use a slightly different, future timezone-aware datetime string
        entry_ts_aware = timezone.make_aware(datetime(2025, 4, 27, 12, 0, 0), timezone.get_default_timezone())
        entry_ts_str = entry_ts_aware.strftime('%Y-%m-%d %H:%M:%S') # Format matching form widget if needed

        form_data = {
            'ticker': 'NEWLOG', 'strategy': 'Classic Breakout', 'entry_date': entry_ts_str,
            'entry_price': '150.50', 'initial_stop_loss': '145.00', 'planned_target': '160.00',
            'position_size': '50', 'user_risk_percent': '1.0',
            'account_capital_at_trade': '50000.00', 'rationale': 'New trade entry.',
            'exit_date': '', 'exit_price': '',
            'emotion_pre': 'Hopeful', 'mistakes': 'None yet', 'lessons': '',
            'emotion_during': '', 'emotion_post': '', 'pnl': '' # Ensure all fields expected by ModelForm are present
        }
        initial_count = TradeLog.objects.count()
        response = self.client.post(self.create_url, form_data, follow=False) # Use follow=False to check redirect easily

        # Check if form is valid (debugging assertion)
        if response.status_code == 200 and 'form' in response.context:
             print("Form Errors:", response.context['form'].errors.as_json())

        assert response.status_code == 302, f"Expected redirect (302), got {response.status_code}"
        assert response.url == self.list_url, f"Expected redirect to {self.list_url}, got {response.url}"
        assert TradeLog.objects.count() == initial_count + 1, "TradeLog count did not increase"
        assert TradeLog.objects.filter(ticker='NEWLOG').exists(), "TradeLog with ticker NEWLOG was not created"
        # Verify calculated fields if applicable (depends on view logic)
        new_log = TradeLog.objects.get(ticker='NEWLOG')
        assert new_log.planned_rr_ratio is not None # Check if calculation happened

    # REMOVED SKIP
    def test_trade_log_create_view_post_invalid(self):
        """ Test POST request with invalid data for creating a trade log. """
        form_data = {'ticker': 'INVALID'} # Missing many required fields
        initial_count = TradeLog.objects.count()
        response = self.client.post(self.create_url, form_data)

        assert response.status_code == 200, f"Expected re-render (200), got {response.status_code}"
        assert 'form' in response.context
        assert isinstance(response.context['form'], TradeLogForm)
        assert not response.context['form'].is_valid(), "Form should be invalid" # Form should have errors
        assert len(response.context['form'].errors) > 0, "Expected form errors, found none"
        # Check specific field errors if needed, e.g.:
        assert 'strategy' in response.context['form'].errors
        assert 'entry_date' in response.context['form'].errors
        assert 'entry_price' in response.context['form'].errors

        assert 'dashboard/trade_log_form.html' in [t.name for t in response.templates]
        assert TradeLog.objects.count() == initial_count, "TradeLog count should not increase on invalid POST"
        assert not TradeLog.objects.filter(ticker='INVALID').exists()

    # --- Detail View Tests ---
    def test_trade_log_detail_view_get(self):
        """ Test GET request for the trade log detail view. """
        response = self.client.get(self.detail_url)
        assert response.status_code == 200
        assert 'trade_log' in response.context
        assert response.context['trade_log'] == self.trade_log
        assert 'dashboard/trade_log_detail.html' in [t.name for t in response.templates]
        # Add check for checklist items if applicable to detail view context
        assert 'checklist_items' in response.context

    def test_trade_log_detail_view_not_found(self):
        """ Test GET request for a non-existent trade log detail. """
        url = reverse('dashboard:trade_log_detail', kwargs={'pk': 9999}) # Non-existent PK
        response = self.client.get(url)
        assert response.status_code == 404

    # --- Update View Tests ---
    def test_trade_log_update_view_get(self):
        """ Test GET request for the trade log update view. """
        response = self.client.get(self.update_url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], TradeLogForm)
        assert response.context['form'].instance == self.trade_log # Form should be bound
        assert 'dashboard/trade_log_form.html' in [t.name for t in response.templates]

    # REMOVED SKIP
    def test_trade_log_update_view_post_valid(self):
        """ Test the trade log update view with valid POST data. """
        exit_ts_aware = timezone.make_aware(datetime(2025, 4, 27, 14, 0, 0), timezone.get_default_timezone())
        exit_ts_str = exit_ts_aware.strftime('%Y-%m-%d %H:%M:%S')

        update_data = {
            'ticker': self.trade_log.ticker, 'strategy': 'Updated Strategy',
            'entry_date': self.trade_log.entry_date.strftime('%Y-%m-%d %H:%M:%S'), # Format consistently
            'entry_price': str(self.trade_log.entry_price),
            'exit_date': exit_ts_str,
            'exit_price': '110.00',
            'initial_stop_loss': str(self.trade_log.initial_stop_loss), 'planned_target': '120.00', # Added planned target
            'position_size': str(self.trade_log.position_size),
            'user_risk_percent': str(self.trade_log.user_risk_percent),
            'account_capital_at_trade': str(self.trade_log.account_capital_at_trade),
            'rationale': 'Updated rationale', 'lessons': 'Learned something',
            'emotion_pre': '', 'emotion_during': '', 'emotion_post': '', # Include all form fields
            'mistakes': '', 'pnl': '100.00' # Example PNL
        }
        response = self.client.post(self.update_url, update_data, follow=False)

        # Debugging if test fails
        if response.status_code == 200 and 'form' in response.context:
             print("Update Form Errors:", response.context['form'].errors.as_json())

        assert response.status_code == 302, f"Expected redirect (302), got {response.status_code}"
        assert response.url == self.detail_url, f"Expected redirect to {self.detail_url}, got {response.url}"
        self.trade_log.refresh_from_db()
        assert self.trade_log.strategy == 'Updated Strategy'
        assert self.trade_log.exit_price == Decimal('110.00')
        assert self.trade_log.rationale == 'Updated rationale'
        assert self.trade_log.lessons == 'Learned something'
        assert self.trade_log.pnl == Decimal('100.00') # Check PNL update

    # REMOVED SKIP
    def test_trade_log_update_view_post_invalid(self):
        """ Test POST request with invalid data for updating a trade log. """
        # Need all required fields even when updating with invalid data for one field
        update_data = {
            'ticker': self.trade_log.ticker, 'strategy': self.trade_log.strategy,
            'entry_date': self.trade_log.entry_date.strftime('%Y-%m-%d %H:%M:%S'),
            'entry_price': 'invalid-price', # Invalid value
            'initial_stop_loss': str(self.trade_log.initial_stop_loss),
            'position_size': str(self.trade_log.position_size),
            'user_risk_percent': str(self.trade_log.user_risk_percent),
            'account_capital_at_trade': str(self.trade_log.account_capital_at_trade),
            'rationale': self.trade_log.rationale,
            # Include other fields as needed by the form...
        }
        response = self.client.post(self.update_url, update_data)

        assert response.status_code == 200, f"Expected re-render (200), got {response.status_code}"
        assert 'form' in response.context
        assert not response.context['form'].is_valid()
        assert 'entry_price' in response.context['form'].errors, "Expected error for 'entry_price'"
        assert 'dashboard/trade_log_form.html' in [t.name for t in response.templates]

    # --- Delete View Tests ---
    def test_trade_log_delete_view_get(self):
        """ Test GET request for the trade log delete confirmation view. """
        response = self.client.get(self.delete_url)
        assert response.status_code == 200
        assert 'trade_log' in response.context
        assert response.context['trade_log'] == self.trade_log
        assert 'dashboard/trade_log_confirm_delete.html' in [t.name for t in response.templates]

    # REMOVED SKIP
    def test_trade_log_delete_view_post(self):
        """ Test POST request to delete a trade log. """
        log_pk = self.trade_log.pk
        initial_count = TradeLog.objects.count()
        response = self.client.post(self.delete_url, follow=False) # POST confirms deletion

        assert response.status_code == 302, f"Expected redirect (302), got {response.status_code}"
        assert response.url == self.list_url, f"Expected redirect to {self.list_url}, got {response.url}"
        assert TradeLog.objects.count() == initial_count - 1, "TradeLog count did not decrease"
        with pytest.raises(TradeLog.DoesNotExist):
            TradeLog.objects.get(pk=log_pk)
