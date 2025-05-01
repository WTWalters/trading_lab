"""
Unit tests for the risk calculator integration with the views.
"""

from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from dashboard.models import TradeLog
from core.risk_calculator import calculate_rr_ratio, calculate_position_size


class TestRiskCalculatorInViews(TestCase):
    """Test case for the risk calculator integration with views."""
    
    def test_trade_log_create_with_risk_calculations(self):
        """Test that risk calculations are saved when creating a trade log."""
        trade_data = {
            'ticker': 'AAPL',
            'strategy': 'Classic Breakout',
            'entry_date': '2023-01-01T10:00:00',
            'entry_price': '150.00',
            'initial_stop_loss': '145.00',
            'planned_target': '160.00',
            'position_size': '100',
            'user_risk_percent': '1.00',
            'account_capital_at_trade': '100000.00',
            'rationale': 'Test rationale',
            # Not providing planned_rr_ratio or suggested_position_size
            # to test automatic calculation
        }
        
        # Submit the form
        response = self.client.post(reverse('dashboard:trade_log_create'), trade_data, follow=True)
        
        # Check that the form was submitted successfully
        self.assertEqual(response.status_code, 200)
        
        # Check that a TradeLog was created
        self.assertEqual(TradeLog.objects.count(), 1)
        
        # Get the created trade log
        trade_log = TradeLog.objects.first()
        
        # Expected calculated values
        expected_rr_ratio = calculate_rr_ratio(
            Decimal('150.00'), Decimal('145.00'), Decimal('160.00')
        )
        expected_position_size = calculate_position_size(
            Decimal('100000.00'), Decimal('1.00'), Decimal('150.00'), Decimal('145.00')
        )
        
        # Check that the risk calculations were saved
        self.assertEqual(trade_log.planned_rr_ratio, expected_rr_ratio)
        self.assertEqual(trade_log.suggested_position_size, expected_position_size)
    
    def test_trade_log_create_with_provided_risk_values(self):
        """Test that provided risk values are used when creating a trade log."""
        trade_data = {
            'ticker': 'AAPL',
            'strategy': 'Classic Breakout',
            'entry_date': '2023-01-01T10:00:00',
            'entry_price': '150.00',
            'initial_stop_loss': '145.00',
            'planned_target': '160.00',
            'position_size': '100',
            'user_risk_percent': '1.00',
            'account_capital_at_trade': '100000.00',
            'rationale': 'Test rationale',
            'planned_rr_ratio': '2.50',  # Provided value
            'suggested_position_size': '250',  # Provided value
        }
        
        # Submit the form
        response = self.client.post(reverse('dashboard:trade_log_create'), trade_data, follow=True)
        
        # Check that the form was submitted successfully
        self.assertEqual(response.status_code, 200)
        
        # Check that a TradeLog was created
        self.assertEqual(TradeLog.objects.count(), 1)
        
        # Get the created trade log
        trade_log = TradeLog.objects.first()
        
        # Check that the provided risk values were used
        self.assertEqual(trade_log.planned_rr_ratio, Decimal('2.50'))
        self.assertEqual(trade_log.suggested_position_size, Decimal('250'))
    
    def test_trade_log_update_with_risk_calculations(self):
        """Test that risk calculations are updated when updating a trade log."""
        # Create a trade log
        trade_log = TradeLog.objects.create(
            ticker='AAPL',
            strategy='Classic Breakout',
            entry_date='2023-01-01T10:00:00',
            entry_price=Decimal('150.00'),
            initial_stop_loss=Decimal('145.00'),
            planned_target=Decimal('160.00'),
            position_size=Decimal('100'),
            user_risk_percent=Decimal('1.00'),
            account_capital_at_trade=Decimal('100000.00'),
            rationale='Test rationale',
            planned_rr_ratio=Decimal('2.00'),
            suggested_position_size=Decimal('200'),
        )
        
        # Updated data with different price values
        updated_data = {
            'ticker': 'AAPL',
            'strategy': 'Classic Breakout',
            'entry_date': '2023-01-01T10:00:00',
            'entry_price': '160.00',  # Changed
            'initial_stop_loss': '155.00',  # Changed
            'planned_target': '170.00',  # Changed
            'position_size': '100',
            'user_risk_percent': '1.00',
            'account_capital_at_trade': '100000.00',
            'rationale': 'Test rationale',
            # Not providing planned_rr_ratio or suggested_position_size
            # to test automatic recalculation
        }
        
        # Submit the form
        response = self.client.post(
            reverse('dashboard:trade_log_update', kwargs={'pk': trade_log.pk}),
            updated_data,
            follow=True
        )
        
        # Check that the form was submitted successfully
        self.assertEqual(response.status_code, 200)
        
        # Get the updated trade log
        trade_log.refresh_from_db()
        
        # Expected calculated values
        expected_rr_ratio = calculate_rr_ratio(
            Decimal('160.00'), Decimal('155.00'), Decimal('170.00')
        )
        expected_position_size = calculate_position_size(
            Decimal('100000.00'), Decimal('1.00'), Decimal('160.00'), Decimal('155.00')
        )
        
        # Check that the risk calculations were updated
        self.assertEqual(trade_log.planned_rr_ratio, expected_rr_ratio)
        self.assertEqual(trade_log.suggested_position_size, expected_position_size)
