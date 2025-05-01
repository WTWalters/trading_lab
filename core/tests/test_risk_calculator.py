"""
Unit tests for the risk calculator module.
"""

import unittest
from decimal import Decimal

from core.risk_calculator import calculate_rr_ratio, calculate_position_size


class TestRiskCalculator(unittest.TestCase):
    """Test case for the risk calculator functions."""
    
    def test_calculate_rr_ratio(self):
        """Test the calculate_rr_ratio function with various inputs."""
        # Test with a 1:2 risk/reward ratio (long position)
        self.assertEqual(calculate_rr_ratio(100, 95, 110), Decimal('2.00'))
        
        # Test with a 1:3 risk/reward ratio (short position)
        self.assertEqual(calculate_rr_ratio(100, 110, 70), Decimal('3.00'))
        
        # Test with decimal values
        self.assertEqual(calculate_rr_ratio(100.5, 97.5, 109.0), Decimal('2.83'))
        
        # Test with Decimal objects
        self.assertEqual(
            calculate_rr_ratio(Decimal('100'), Decimal('90'), Decimal('120')),
            Decimal('2.00')
        )
        
        # Test with zero risk (entry = stop)
        self.assertIsNone(calculate_rr_ratio(100, 100, 110))
        
        # Test with zero reward (entry = target)
        self.assertIsNone(calculate_rr_ratio(100, 95, 100))
        
        # Test with invalid inputs
        self.assertIsNone(calculate_rr_ratio(None, 95, 110))
        self.assertIsNone(calculate_rr_ratio(100, None, 110))
        self.assertIsNone(calculate_rr_ratio(100, 95, None))
        self.assertIsNone(calculate_rr_ratio('invalid', 95, 110))
    
    def test_calculate_position_size(self):
        """Test the calculate_position_size function with various inputs."""
        # Test with 1% risk on a $100,000 account with $5 risk per share
        self.assertEqual(
            calculate_position_size(100000, 1, 100, 95),
            Decimal('200')
        )
        
        # Test with 2% risk on a $50,000 account with $2.5 risk per share
        self.assertEqual(
            calculate_position_size(50000, 2, 50, 47.5),
            Decimal('400')
        )
        
        # Test with Decimal objects
        self.assertEqual(
            calculate_position_size(
                Decimal('100000'), Decimal('1.5'), 
                Decimal('200'), Decimal('190')
            ),
            Decimal('150')
        )
        
        # Test with zero risk per share
        self.assertIsNone(calculate_position_size(100000, 1, 100, 100))
        
        # Test with invalid inputs
        self.assertIsNone(calculate_position_size(None, 1, 100, 95))
        self.assertIsNone(calculate_position_size(100000, None, 100, 95))
        self.assertIsNone(calculate_position_size(100000, 1, None, 95))
        self.assertIsNone(calculate_position_size(100000, 1, 100, None))
        self.assertIsNone(calculate_position_size('invalid', 1, 100, 95))


if __name__ == '__main__':
    unittest.main()
