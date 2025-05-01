"""
Manual test for risk calculator functions.
"""

from decimal import Decimal
from core.risk_calculator import calculate_rr_ratio, calculate_position_size

def test_calculate_rr_ratio():
    # Test case 1: Regular calculation (1:2 R:R for long trade)
    entry = Decimal('100')
    stop = Decimal('95')
    target = Decimal('110')
    result = calculate_rr_ratio(entry, stop, target)
    print(f"Test calculate_rr_ratio(100, 95, 110) = {result} (Expected: 2.00)")
    
    # Test case 2: Short trade
    entry = Decimal('100')
    stop = Decimal('105')
    target = Decimal('90')
    result = calculate_rr_ratio(entry, stop, target)
    print(f"Test calculate_rr_ratio(100, 105, 90) = {result} (Expected: 2.00)")
    
    # Test case 3: Edge case (division by zero)
    entry = Decimal('100')
    stop = Decimal('100')
    target = Decimal('110')
    result = calculate_rr_ratio(entry, stop, target)
    print(f"Test calculate_rr_ratio(100, 100, 110) = {result} (Expected: None)")

def test_calculate_position_size():
    # Test case 1: Regular calculation
    capital = Decimal('100000')
    risk_pct = Decimal('1')
    entry = Decimal('100')
    stop = Decimal('95')
    result = calculate_position_size(capital, risk_pct, entry, stop)
    print(f"Test calculate_position_size(100000, 1, 100, 95) = {result} (Expected: 200)")
    
    # Test case 2: Different risk percentage
    capital = Decimal('100000')
    risk_pct = Decimal('2')
    entry = Decimal('100')
    stop = Decimal('95')
    result = calculate_position_size(capital, risk_pct, entry, stop)
    print(f"Test calculate_position_size(100000, 2, 100, 95) = {result} (Expected: 400)")
    
    # Test case 3: Edge case (division by zero)
    capital = Decimal('100000')
    risk_pct = Decimal('1')
    entry = Decimal('100')
    stop = Decimal('100')
    result = calculate_position_size(capital, risk_pct, entry, stop)
    print(f"Test calculate_position_size(100000, 1, 100, 100) = {result} (Expected: None)")

if __name__ == "__main__":
    print("Testing calculate_rr_ratio:")
    test_calculate_rr_ratio()
    print("\nTesting calculate_position_size:")
    test_calculate_position_size()
