# dashboard/forms.py
from django import forms
from .models import TradeLog

class TradeLogForm(forms.ModelForm):
    """
    Form for creating and editing Trade Log entries.
    Provides user-friendly widgets and validation for the TradeLog model.
    """
    class Meta:
        model = TradeLog
        fields = [
            'ticker', 'strategy', 'entry_date', 'exit_date',
            'entry_price', 'exit_price', 'initial_stop_loss', 'planned_target',
            'position_size', 'user_risk_percent', 'account_capital_at_trade',
            'pnl', # <--- ADDED PNL HERE
            'planned_rr_ratio', 'suggested_position_size',
            'rationale', 'emotion_pre', 'emotion_during', 'emotion_post',
            'mistakes', 'lessons'
        ]
        widgets = {
            'entry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'exit_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'entry_price': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 150.75'}),
            'exit_price': forms.NumberInput(attrs={'step': '0.0001'}),
            'initial_stop_loss': forms.NumberInput(attrs={'step': '0.0001'}),
            'planned_target': forms.NumberInput(attrs={'step': '0.0001'}),
            'position_size': forms.NumberInput(attrs={'step': '0.01'}),
            'user_risk_percent': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'max': '10'}),
            'account_capital_at_trade': forms.NumberInput(attrs={'step': '1'}),
            'pnl': forms.NumberInput(attrs={'step': '0.01'}), # Optional: Add widget for consistency
            'planned_rr_ratio': forms.NumberInput(attrs={'step': '0.01'}),
            'suggested_position_size': forms.NumberInput(attrs={'step': '1'}),
            'rationale': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Why did you enter this trade?'}),
            'emotion_pre': forms.Textarea(attrs={'rows': 2}),
            'emotion_during': forms.Textarea(attrs={'rows': 2}),
            'emotion_post': forms.Textarea(attrs={'rows': 2}),
            'mistakes': forms.Textarea(attrs={'rows': 2}),
            'lessons': forms.Textarea(attrs={'rows': 2}),
            'ticker': forms.TextInput(attrs={'placeholder': 'e.g., AAPL'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call super first

        common_form_control_class = 'form-control'
        select_class = 'form-select'

        for field_name, field in self.fields.items():
            widget = field.widget
            current_attrs = widget.attrs or {}
            existing_classes = current_attrs.get('class', '')
            target_class = select_class if isinstance(widget, forms.Select) else common_form_control_class
            if target_class not in existing_classes.split():
                current_attrs['class'] = f'{existing_classes} {target_class}'.strip()

        self.fields['strategy'].widget = forms.Select(
            choices=[
                ('', '---------'),
                ('Classic Breakout', 'Classic Breakout'),
                ('Moving Average Crossover', 'Moving Average Crossover'),
                ('Support/Resistance', 'Support/Resistance'),
                ('Other', 'Other')
            ],
            attrs={'class': select_class}
        )

        self.fields['ticker'].widget.attrs.setdefault('placeholder', 'e.g., AAPL')
        self.fields['entry_price'].widget.attrs.setdefault('placeholder', 'e.g., 150.75')
        self.fields['rationale'].widget.attrs.setdefault('placeholder', 'Why did you enter this trade?')
