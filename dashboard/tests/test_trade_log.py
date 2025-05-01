# dashboard/tests/test_trade_log.py
from django.test import TestCase
from django.utils import timezone
from django import forms
from decimal import Decimal
from dashboard.models import TradeLog
from dashboard.forms import TradeLogForm

class TradeLogModelTest(TestCase):
    """Test cases for the TradeLog model"""
    
    def setUp(self):
        """Set up test data for the TradeLog model tests"""
        self.trade_log = TradeLog.objects.create(
            ticker="AAPL",
            strategy="Classic Breakout",
            entry_date=timezone.now(),
            entry_price=Decimal("150.50"),
            initial_stop_loss=Decimal("145.00"),
            planned_target=Decimal("160.00"),
            position_size=Decimal("100"),
            user_risk_percent=Decimal("2.00"),
            account_capital_at_trade=Decimal("10000.00"),
            rationale="Strong breakout with volume confirmation"
        )
    
    def test_trade_log_creation(self):
        """Test that a TradeLog instance can be created successfully"""
        self.assertIsInstance(self.trade_log, TradeLog)
        self.assertEqual(self.trade_log.ticker, "AAPL")
        self.assertEqual(self.trade_log.strategy, "Classic Breakout")
        self.assertEqual(self.trade_log.entry_price, Decimal("150.50"))
        self.assertEqual(self.trade_log.initial_stop_loss, Decimal("145.00"))
        self.assertEqual(self.trade_log.planned_target, Decimal("160.00"))
        self.assertEqual(self.trade_log.position_size, Decimal("100"))
        self.assertEqual(self.trade_log.user_risk_percent, Decimal("2.00"))
        self.assertEqual(self.trade_log.account_capital_at_trade, Decimal("10000.00"))
        self.assertEqual(self.trade_log.rationale, "Strong breakout with volume confirmation")
    
    def test_trade_log_string_representation(self):
        """Test the string representation of a TradeLog instance"""
        expected_string = f"AAPL trade on {self.trade_log.entry_date.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.trade_log), expected_string)
    
    def test_trade_log_optional_fields(self):
        """Test that optional fields can be left empty"""
        # These fields should be None by default
        self.assertIsNone(self.trade_log.exit_date)
        self.assertIsNone(self.trade_log.exit_price)
        self.assertIsNone(self.trade_log.pnl)
        self.assertIsNone(self.trade_log.emotion_pre)
        self.assertIsNone(self.trade_log.emotion_during)
        self.assertIsNone(self.trade_log.emotion_post)
        self.assertIsNone(self.trade_log.mistakes)
        self.assertIsNone(self.trade_log.lessons)
        
        # Update with optional fields
        self.trade_log.exit_date = timezone.now()
        self.trade_log.exit_price = Decimal("155.25")
        self.trade_log.pnl = Decimal("475.00")  # (155.25 - 150.50) * 100
        self.trade_log.emotion_pre = "Confident"
        self.trade_log.save()
        
        # Refresh from database
        self.trade_log.refresh_from_db()
        
        # Check values
        self.assertIsNotNone(self.trade_log.exit_date)
        self.assertEqual(self.trade_log.exit_price, Decimal("155.25"))
        self.assertEqual(self.trade_log.pnl, Decimal("475.00"))
        self.assertEqual(self.trade_log.emotion_pre, "Confident")


class TradeLogFormTest(TestCase):
    """Test cases for the TradeLogForm"""
    
    def test_valid_form(self):
        """Test that the form is valid with all required fields"""
        data = {
            'ticker': "TSLA",
            'strategy': "Classic Breakout",
            'entry_date': timezone.now(),
            'entry_price': "220.50",
            'initial_stop_loss': "210.00",
            'planned_target': "240.00",
            'position_size': "50",
            'user_risk_percent': "1.50",
            'account_capital_at_trade': "20000.00",
            'rationale': "Breaking out of consolidation with strong volume"
        }
        form = TradeLogForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_required_fields(self):
        """Test that the form is invalid when required fields are missing"""
        data = {
            'ticker': "TSLA",
            # Missing other required fields
        }
        form = TradeLogForm(data=data)
        self.assertFalse(form.is_valid())
        # Check that the form has errors for the missing fields
        self.assertIn('entry_date', form.errors)
        self.assertIn('entry_price', form.errors)
        self.assertIn('initial_stop_loss', form.errors)
        self.assertIn('position_size', form.errors)
        self.assertIn('user_risk_percent', form.errors)
        self.assertIn('account_capital_at_trade', form.errors)
        self.assertIn('rationale', form.errors)
    
    def test_form_field_types(self):
        """Test that form fields have appropriate widgets"""
        form = TradeLogForm()
        
        # Test numeric fields have number inputs
        self.assertIsInstance(form.fields['entry_price'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['exit_price'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['initial_stop_loss'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['planned_target'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['position_size'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['user_risk_percent'].widget, forms.NumberInput)
        
        # Test text fields have text areas
        self.assertIsInstance(form.fields['rationale'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['emotion_pre'].widget, forms.Textarea)
