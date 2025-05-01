"""
Core strategies module defining trading strategies for backtesting.

This module implements trading strategies using the Backtrader framework.
Currently implements:
- ClassicBreakoutStrategy: A strategy based on price consolidation breakouts
  with volume confirmation and ATR-based stop management.
"""
import logging
import backtrader as bt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClassicBreakoutStrategy(bt.Strategy):
    """
    Classic Breakout Strategy

    This strategy identifies consolidation ranges and detects breakouts based on price
    and volume. It uses ATR for initial stop-loss placement and implements a
    Chandelier Exit (ATR-based trailing stop) for position management.

    Strategy Logic:
    1. Identify consolidation ranges over a defined lookback period
    2. Detect breakouts with volume confirmation
    3. Enter on the next bar after a confirmed breakout
    4. Set initial stop-loss based on ATR
    5. Trail stop using Chandelier Exit mechanism
    """

    params = (
        ('lookback', 50),  # Number of periods to look back for consolidation range
        ('volume_ma_period', 20),  # Period for volume moving average
        ('volume_mult', 1.5),  # Volume must be > this multiple of volume MA
        ('atr_period', 14),  # Period for ATR calculation
        ('initial_stop_atr_mult', 2.0),  # Initial stop = Entry - (ATR * this value)
        ('trail_stop_atr_mult', 3.0),  # Trailing stop = Highest High - (ATR * this value)
    )

    def log(self, txt, dt=None):
        """Logger for the strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        logger.info(f'{dt.isoformat()} - {txt}')

    def __init__(self):
        """Initialize strategy components."""
        # Data series
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataopen = self.datas[0].open
        self.datavolume = self.datas[0].volume

        # Indicators
        self.atr = bt.indicators.ATR(self.datas[0], period=self.p.atr_period)
        self.vol_ma = bt.indicators.SMA(self.datavolume, period=self.p.volume_ma_period)

        # Trade management
        self.order = None  # Current pending order
        self.entry_price = None  # Price at which we entered
        self.initial_stop_price = None  # Initial stop price
        self.highest_high_since_entry = None  # Highest high since we entered
        self.trailing_stop_price = None  # Current trailing stop price

    def notify_order(self, order):
        """Handle order notifications."""
        if order.status in [order.Submitted, order.Accepted]:
            # Order just submitted/accepted - no action required
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}')
                # Record entry details
                self.entry_price = order.executed.price
                self.highest_high_since_entry = self.datahigh[0]
                # Set initial stop loss
                self.initial_stop_price = self.entry_price - (self.atr[0] * self.p.initial_stop_atr_mult)
                self.trailing_stop_price = self.initial_stop_price
                self.log(f'INITIAL STOP SET AT: {self.initial_stop_price:.2f}')
            else:  # Sell
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}')
                # Reset entry tracking variables
                self.entry_price = None
                self.highest_high_since_entry = None
                self.initial_stop_price = None
                self.trailing_stop_price = None

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected: {order.status}')

        # Reset order reference
        self.order = None

    def notify_trade(self, trade):
        """Handle trade notifications."""
        if not trade.isclosed:
            return

        self.log(f'TRADE CLOSED - Profit: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')

    def next(self):
        """Main strategy logic executed on each bar."""
        # Skip if we have a pending order
        if self.order:
            return

        # Check if we are in a position
        if not self.position:
            # No position - check for entry signals

            # 1. Identify consolidation range
            high_range = max([self.datahigh[-i] for i in range(1, min(self.p.lookback + 1, len(self)))])
            low_range = min([self.datalow[-i] for i in range(1, min(self.p.lookback + 1, len(self)))])

            # 2. Check for a breakout with volume confirmation
            # Breakout is when price closes above the recent high range
            breakout_up = self.dataclose[0] > high_range
            # Confirm with volume
            volume_confirmed = self.datavolume[0] > (self.vol_ma[0] * self.p.volume_mult)

            # 3. If breakout is confirmed, generate buy signal for next bar
            if breakout_up and volume_confirmed:
                self.log('BUY SIGNAL - Breakout Confirmed')
                # Execute buy order with next bar market order
                self.order = self.buy()
        else:
            # In a position - check for exit signals
            
            # Update highest high since entry
            if self.datahigh[0] > self.highest_high_since_entry:
                self.highest_high_since_entry = self.datahigh[0]
                # Update trailing stop price (Chandelier Exit)
                new_stop = self.highest_high_since_entry - (self.atr[0] * self.p.trail_stop_atr_mult)
                # Only raise the stop, never lower it
                if new_stop > self.trailing_stop_price:
                    self.trailing_stop_price = new_stop
                    self.log(f'TRAILING STOP RAISED TO: {self.trailing_stop_price:.2f}')

            # Check if stop is hit
            if self.dataclose[0] < self.trailing_stop_price:
                self.log('SELL SIGNAL - Trailing Stop Hit')
                # Execute sell order
                self.order = self.sell()
