"""
Manual test for the backend risk calculation and saving functionality.
This script simulates what happens in the view when a trade log is saved.
"""

from decimal import Decimal
from core.risk_calculator import calculate_rr_ratio, calculate_position_size

class CleanedData:
    """Simulate form.cleaned_data dict-like access."""
    def __init__(self, data):
        self.data = data
    
    def get(self, key, default=None):
        return self.data.get(key, default)

class FormInstance:
    """Simulate form.instance object."""
    def __init__(self):
        self.planned_rr_ratio = None
        self.suggested_position_size = None

class MockForm:
    """Simulate a Django form with cleaned_data and instance."""
    def __init__(self, post_data):
        self.cleaned_data = CleanedData(post_data)
        self.instance = FormInstance()

def simulate_view_save_logic(form):
    """Simulate the risk calculation logic from the view."""
    # Extract values from cleaned_data (as done in the view)
    entry_price = form.cleaned_data.get('entry_price')
    stop_loss = form.cleaned_data.get('initial_stop_loss')
    target_price = form.cleaned_data.get('planned_target')
    risk_percent = form.cleaned_data.get('user_risk_percent')
    account_capital = form.cleaned_data.get('account_capital_at_trade')
    
    # Set planned_rr_ratio if not already set in the form
    if not form.cleaned_data.get('planned_rr_ratio') and entry_price and stop_loss and target_price:
        form.instance.planned_rr_ratio = calculate_rr_ratio(entry_price, stop_loss, target_price)
    else:
        # If provided in form, use that value
        form.instance.planned_rr_ratio = form.cleaned_data.get('planned_rr_ratio')
    
    # Set suggested_position_size if not already set in the form
    if not form.cleaned_data.get('suggested_position_size') and entry_price and stop_loss and risk_percent and account_capital:
        form.instance.suggested_position_size = calculate_position_size(
            account_capital, risk_percent, entry_price, stop_loss
        )
    else:
        # If provided in form, use that value
        form.instance.suggested_position_size = form.cleaned_data.get('suggested_position_size')
    
    # Return what would be saved to the database
    return {
        'planned_rr_ratio': form.instance.planned_rr_ratio,
        'suggested_position_size': form.instance.suggested_position_size
    }

def test_backend_calculations():
    """Test the backend risk calculation logic."""
    # Test Case 1: No values provided in form - should calculate
    post_data1 = {
        'entry_price': Decimal('100'),
        'initial_stop_loss': Decimal('95'),
        'planned_target': Decimal('110'),
        'user_risk_percent': Decimal('1'),
        'account_capital_at_trade': Decimal('100000'),
        # planned_rr_ratio and suggested_position_size not provided
    }
    
    form1 = MockForm(post_data1)
    result1 = simulate_view_save_logic(form1)
    print("Test Case 1 - Calculate both values:")
    print(f"  planned_rr_ratio: {result1['planned_rr_ratio']} (Expected: 2.00)")
    print(f"  suggested_position_size: {result1['suggested_position_size']} (Expected: 200)")
    
    # Test Case 2: Values provided in form - should use provided values
    post_data2 = {
        'entry_price': Decimal('100'),
        'initial_stop_loss': Decimal('95'),
        'planned_target': Decimal('110'),
        'user_risk_percent': Decimal('1'),
        'account_capital_at_trade': Decimal('100000'),
        'planned_rr_ratio': Decimal('3.00'),  # Provided, but doesn't match calculations
        'suggested_position_size': Decimal('300'),  # Provided, but doesn't match calculations
    }
    
    form2 = MockForm(post_data2)
    result2 = simulate_view_save_logic(form2)
    print("\nTest Case 2 - Use provided values:")
    print(f"  planned_rr_ratio: {result2['planned_rr_ratio']} (Expected: 3.00)")
    print(f"  suggested_position_size: {result2['suggested_position_size']} (Expected: 300)")
    
    # Test Case 3: Missing some values - should handle gracefully
    post_data3 = {
        'entry_price': Decimal('100'),
        'initial_stop_loss': Decimal('95'),
        # planned_target missing
        'user_risk_percent': Decimal('1'),
        'account_capital_at_trade': Decimal('100000'),
    }
    
    form3 = MockForm(post_data3)
    result3 = simulate_view_save_logic(form3)
    print("\nTest Case 3 - Missing target price:")
    print(f"  planned_rr_ratio: {result3['planned_rr_ratio']} (Expected: None)")
    print(f"  suggested_position_size: {result3['suggested_position_size']} (Expected: 200)")

if __name__ == "__main__":
    test_backend_calculations()
