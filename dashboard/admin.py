from django.contrib import admin
from .models import OHLCVData, TradeLog, TradeChecklistStatus

# Register the OHLCVData model
@admin.register(OHLCVData)
class OHLCVDataAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'timestamp', 'open', 'high', 'low', 'close', 'volume')
    list_filter = ('ticker',)
    search_fields = ('ticker',)
    date_hierarchy = 'timestamp'

# Register the TradeLog model
@admin.register(TradeLog)
class TradeLogAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'strategy', 'entry_date', 'entry_price', 'exit_date', 'exit_price', 'pnl')
    list_filter = ('ticker', 'strategy')
    search_fields = ('ticker', 'rationale', 'lessons')
    date_hierarchy = 'entry_date'
    
    fieldsets = (
        ('Trade Basics', {
            'fields': ('ticker', 'strategy', 'entry_date', 'exit_date')
        }),
        ('Price Information', {
            'fields': ('entry_price', 'exit_price', 'initial_stop_loss', 'planned_target')
        }),
        ('Position & Risk', {
            'fields': ('position_size', 'suggested_position_size', 'user_risk_percent', 
                      'account_capital_at_trade', 'planned_rr_ratio', 'pnl')
        }),
        ('Trade Analysis', {
            'fields': ('rationale', 'emotion_pre', 'emotion_during', 'emotion_post', 
                      'mistakes', 'lessons')
        }),
    )


# Register the TradeChecklistStatus model as inline for TradeLog
class TradeChecklistStatusInline(admin.TabularInline):
    model = TradeChecklistStatus
    extra = 0


# Add the inline to TradeLogAdmin
TradeLogAdmin.inlines = [TradeChecklistStatusInline]


# Also register TradeChecklistStatus as a standalone model
@admin.register(TradeChecklistStatus)
class TradeChecklistStatusAdmin(admin.ModelAdmin):
    list_display = ('trade_log', 'checklist_item', 'is_checked')
    list_filter = ('is_checked', 'checklist_item')
    search_fields = ('trade_log__ticker', 'checklist_item')
    list_editable = ('is_checked',)
