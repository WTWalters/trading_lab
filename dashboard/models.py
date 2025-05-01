# dashboard/models.py
from django.db import models
from django.utils import timezone

class OHLCVData(models.Model):
    """
    Stores daily OHLCV data. Uses default Django ID PK.
    Hypertable conversion and indexing managed manually in migrations.
    """
    # Default 'id' PK will be created by Django
    timestamp = models.DateTimeField(
        help_text="The beginning of the time interval (e.g., day) for the OHLCV data."
    )
    ticker = models.CharField(
        max_length=20,
        help_text="Stock ticker symbol (e.g., AAPL)."
    )
    open = models.DecimalField(max_digits=19, decimal_places=4, help_text="...")
    high = models.DecimalField(max_digits=19, decimal_places=4, help_text="...")
    low = models.DecimalField(max_digits=19, decimal_places=4, help_text="...")
    close = models.DecimalField(max_digits=19, decimal_places=4, help_text="...")
    volume = models.BigIntegerField(help_text="...")

    class Meta:
        verbose_name = "OHLCV Data"
        verbose_name_plural = "OHLCV Data"
        ordering = ['ticker', '-timestamp']
        # NO CONSTRAINTS OR INDEXES DEFINED HERE

    def __str__(self):
        # ... (same) ...
        ts_formatted = timezone.localtime(self.timestamp).strftime('%Y-%m-%d %H:%M:%S %Z') if self.timestamp else 'N/A'
        return f"{self.ticker} @ {ts_formatted}"


class TradeLog(models.Model):
    """
    Stores user-logged trade details with financial, strategic and psychological information.
    This model serves as a trade journal to help users track their trading activity and psychology.
    """
    # Trade identifiers and basic details
    ticker = models.CharField(
        max_length=20,
        help_text="Stock ticker symbol (e.g., AAPL)"
    )
    strategy = models.CharField(
        max_length=50,
        help_text="Trading strategy used (e.g., Classic Breakout)"
    )
    
    # Trade timing
    entry_date = models.DateTimeField(
        help_text="Date and time when the trade was entered"
    )
    exit_date = models.DateTimeField(
        null=True, blank=True,
        help_text="Date and time when the trade was exited (can be filled later)"
    )
    
    # Price levels
    entry_price = models.DecimalField(
        max_digits=19, decimal_places=4,
        help_text="Price at which the trade was entered"
    )
    exit_price = models.DecimalField(
        max_digits=19, decimal_places=4, null=True, blank=True,
        help_text="Price at which the trade was exited (can be filled later)"
    )
    initial_stop_loss = models.DecimalField(
        max_digits=19, decimal_places=4,
        help_text="Initial stop loss price"
    )
    planned_target = models.DecimalField(
        max_digits=19, decimal_places=4, null=True, blank=True,
        help_text="Target price for the trade (projected exit)"
    )
    
    # Position details
    position_size = models.DecimalField(
        max_digits=19, decimal_places=4,
        help_text="Size of the position (number of shares/contracts)"
    )
    suggested_position_size = models.DecimalField(
        max_digits=19, decimal_places=4, null=True, blank=True,
        help_text="Calculated suggested position size based on risk parameters"
    )
    
    # Financial metrics
    pnl = models.DecimalField(
        max_digits=19, decimal_places=4, null=True, blank=True,
        help_text="Profit or loss from the trade (can be calculated)"
    )
    planned_rr_ratio = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Planned risk-reward ratio for the trade"
    )
    user_risk_percent = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Percentage of account willing to risk on this trade"
    )
    account_capital_at_trade = models.DecimalField(
        max_digits=19, decimal_places=2,
        help_text="Account capital at the time of the trade"
    )
    
    # Trade rationale and psychological factors
    rationale = models.TextField(
        help_text="Reasons for entering the trade"
    )
    emotion_pre = models.TextField(
        blank=True, null=True,
        help_text="Emotional state before entering the trade"
    )
    emotion_during = models.TextField(
        blank=True, null=True,
        help_text="Emotional state while in the trade"
    )
    emotion_post = models.TextField(
        blank=True, null=True,
        help_text="Emotional state after exiting the trade"
    )
    mistakes = models.TextField(
        blank=True, null=True,
        help_text="Mistakes made during the trade"
    )
    lessons = models.TextField(
        blank=True, null=True,
        help_text="Lessons learned from the trade"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Trade Log"
        verbose_name_plural = "Trade Logs"
        ordering = ['-entry_date']
    
    def __str__(self):
        return f"{self.ticker} trade on {self.entry_date.strftime('%Y-%m-%d')}"


# Define the checklist items for the Classic Breakout strategy
CLASSIC_BREAKOUT_CHECKLIST = [
    "Consolidation identified in price action?",
    "Volume above 1.5x 20-day average?",
    "Price closed above resistance/below support?",
    "ATR-based stop loss set?",
    "Risk-Reward ratio > 2:1?",
    "Position sized according to risk percentage?",
    "Maximum account risk < 2%?"
]


class TradeChecklistStatus(models.Model):
    """
    Stores the status of checklist items for each trade log.
    Each trade log has multiple checklist items, each with a checked/unchecked status.
    """
    trade_log = models.ForeignKey(
        TradeLog, 
        on_delete=models.CASCADE,
        related_name='checklist_items',
        help_text="The trade log this checklist item is associated with"
    )
    checklist_item = models.CharField(
        max_length=255,
        help_text="The checklist item text"
    )
    is_checked = models.BooleanField(
        default=False,
        help_text="Whether the checklist item is checked or not"
    )
    
    class Meta:
        verbose_name = "Trade Checklist Item"
        verbose_name_plural = "Trade Checklist Items"
        unique_together = ('trade_log', 'checklist_item')
        ordering = ['id']  # Maintain the order items were added
    
    def __str__(self):
        status = "✓" if self.is_checked else "✗"
        return f"{status} {self.checklist_item} for {self.trade_log}"
