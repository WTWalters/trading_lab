#core/risk_calculator.py
"""
Core module for calculating trading risk metrics.

This module provides utility functions for calculating risk metrics
in the context of trading, such as Risk:Reward ratio and position sizing
based on account capital and risk percentage.
"""

from decimal import Decimal, InvalidOperation, ROUND_DOWN


def calculate_rr_ratio(entry_price, stop_price, target_price):
    """
    Calculate the Risk:Reward ratio for a trade.

    Args:
        entry_price (float or Decimal): The price at which the trade is entered
        stop_price (float or Decimal): The stop loss price
        target_price (float or Decimal): The target price

    Returns:
        Decimal: The Risk:Reward ratio (reward / risk) rounded to 2 decimal places,
                or None if calculation is not possible
    """
    # Convert to Decimal for precise calculation
    try:
        entry = Decimal(str(entry_price))
        stop = Decimal(str(stop_price))
        target = Decimal(str(target_price))
    except (InvalidOperation, TypeError, ValueError):
        return None

    # Calculate risk (difference between entry and stop)
    risk = abs(entry - stop)

    # Calculate reward (difference between entry and target)
    reward = abs(target - entry)

    # Calculate R:R ratio (avoid division by zero)
    if risk == 0 or reward == 0:
        return None

    # Return the R:R ratio rounded to 2 decimal places
    return (reward / risk).quantize(Decimal('0.01'), rounding=ROUND_DOWN)


def calculate_position_size(account_capital, risk_percent, entry_price, stop_price):
    """
    Calculate the suggested position size based on account capital,
    risk percentage, and price risk per share.

    Args:
        account_capital (float or Decimal): The total account capital
        risk_percent (float or Decimal): The percentage of account willing to risk on this trade
        entry_price (float or Decimal): The price at which the trade is entered
        stop_price (float or Decimal): The stop loss price

    Returns:
        Decimal: The suggested position size (number of shares/contracts) rounded down,
                or None if calculation is not possible
    """
    # Convert to Decimal for precise calculation
    try:
        capital = Decimal(str(account_capital))
        risk_pct = Decimal(str(risk_percent))
        entry = Decimal(str(entry_price))
        stop = Decimal(str(stop_price))
    except (InvalidOperation, TypeError, ValueError):
        return None

    # Calculate risk amount per share
    risk_per_share = abs(entry - stop)

    # Calculate total risk amount (account capital * risk percentage)
    total_risk_amount = capital * (risk_pct / Decimal('100'))

    # Calculate position size (avoid division by zero)
    if risk_per_share == 0:
        return None

    # Calculate and return position size (rounded down to whole shares)
    position_size = (total_risk_amount / risk_per_share).quantize(Decimal('1.'), rounding=ROUND_DOWN)
    return position_size
