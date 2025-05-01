"""
Tests for trading strategies implemented in core/strategies.py
"""
import pytest
import pandas as pd
import backtrader as bt
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch

from core.strategies import ClassicBreakoutStrategy


class TestClassicBreakoutStrategy:
    """Test suite for the ClassicBreakoutStrategy"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        # Create a Cerebro engine
        self.cerebro = bt.Cerebro()
        
        # Add strategy
        self.cerebro.addstrategy(ClassicBreakoutStrategy)
        
        # Set starting cash
        self.cerebro.broker.setcash(100000.0)
        
        # Set commission
        self.cerebro.broker.setcommission(commission=0.001)
        
        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    
    def create_test_data(self, scenario='breakout'):
        """
        Create test data for different scenarios.
        
        Parameters:
            scenario (str): 'breakout', 'no_breakout', 'low_volume'
        
        Returns:
            bt.feeds.PandasData: A Backtrader data feed with test data
        """
        # Create base dates for our data points
        base_date = datetime(2023, 1, 1)
        dates = [base_date + timedelta(days=i) for i in range(100)]
        
        # Create base stock data with a consolidation pattern
        base_price = 100.0
        prices = []
        
        # First 50 days: consolidation between 95-105
        for i in range(50):
            random_offset = np.random.uniform(-5, 5)
            prices.append(base_price + random_offset)
        
        # Next 50 days depend on the scenario
        if scenario == 'breakout':
            # Days 51-55: strong breakout above 105 with high volume
            for i in range(50, 55):
                prices.append(105 + (i - 50) * 2)  # Progressive breakout
            
            # Days 56-99: continue upward but with some volatility
            for i in range(55, 100):
                random_offset = np.random.uniform(-3, 6)
                prices.append(prices[-1] + random_offset)
        
        elif scenario == 'no_breakout':
            # Days 51-99: continue consolidation
            for i in range(50, 100):
                random_offset = np.random.uniform(-5, 5)
                prices.append(base_price + random_offset)
        
        elif scenario == 'low_volume':
            # Days 51-55: price breakout but with insufficient volume
            for i in range(50, 55):
                prices.append(105 + (i - 50) * 2)  # Progressive breakout
            
            # Days 56-99: continue upward but with some volatility
            for i in range(55, 100):
                random_offset = np.random.uniform(-3, 6)
                prices.append(prices[-1] + random_offset)
        
        # Create the DataFrame with OHLCV data
        data = {
            'open': prices,
            'close': prices,  # Simplified: open=close for testing
            'high': [p + np.random.uniform(0, 2) for p in prices],
            'low': [p - np.random.uniform(0, 2) for p in prices],
            'volume': []
        }
        
        # Set volume based on scenario
        for i in range(100):
            if scenario == 'breakout' and i >= 50 and i < 55:
                # High volume during breakout
                data['volume'].append(np.random.uniform(10000, 15000))
            elif scenario == 'low_volume' and i >= 50 and i < 55:
                # Low volume during breakout (below 1.5X average)
                data['volume'].append(np.random.uniform(3000, 4000))
            else:
                # Normal volume
                data['volume'].append(np.random.uniform(5000, 7000))
        
        # Create the DataFrame
        df = pd.DataFrame(data, index=dates)
        
        # Create the Backtrader data feed
        data_feed = bt.feeds.PandasData(dataname=df)
        
        return data_feed
    
    def run_backtest(self, scenario, params=None):
        """
        Run a backtest with the ClassicBreakoutStrategy on the specified scenario.
        
        Parameters:
            scenario (str): The scenario to test ('breakout', 'no_breakout', 'low_volume')
            params (dict): Optional parameters for the strategy
        
        Returns:
            list: List of strategy instances after the backtest
        """
        # Reset Cerebro
        self.cerebro = bt.Cerebro()
        
        # Add strategy with parameters if provided
        if params:
            self.cerebro.addstrategy(ClassicBreakoutStrategy, **params)
        else:
            self.cerebro.addstrategy(ClassicBreakoutStrategy)
        
        # Add test data
        data_feed = self.create_test_data(scenario)
        self.cerebro.adddata(data_feed)
        
        # Set broker
        self.cerebro.broker.setcash(100000.0)
        self.cerebro.broker.setcommission(commission=0.001)
        
        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
        
        # Run backtest
        results = self.cerebro.run()
        
        return results
    
    def test_breakout_detection(self):
        """Test if the strategy detects a valid breakout and enters a position."""
        # Suppress logging during tests
        with patch('logging.Logger.info'):
            results = self.run_backtest('breakout')
        
        # Get trade analyzer
        trade_analyzer = getattr(results[0].analyzers, 'trade_analyzer', None)
        analysis = trade_analyzer.get_analysis() if trade_analyzer else {}
        
        # Check that at least one trade was made
        assert hasattr(analysis, 'total') and analysis.total.total > 0, "No trades were made with a valid breakout"
    
    def test_no_breakout(self):
        """Test that the strategy doesn't enter when there's no breakout."""
        # Suppress logging during tests
        with patch('logging.Logger.info'):
            results = self.run_backtest('no_breakout')
        
        # Get trade analyzer
        trade_analyzer = getattr(results[0].analyzers, 'trade_analyzer', None)
        
        # Check that no trades were made
        # This is a bit tricky because if no trades are made, the analysis might not have a 'total' attribute
        if trade_analyzer:
            analysis = trade_analyzer.get_analysis()
            assert not hasattr(analysis, 'total') or analysis.total.total == 0, "Trades were made when there should be no breakout"
    
    def test_low_volume_rejection(self):
        """Test that the strategy doesn't enter when volume is insufficient."""
        # Suppress logging during tests
        with patch('logging.Logger.info'):
            results = self.run_backtest('low_volume')
        
        # Get trade analyzer
        trade_analyzer = getattr(results[0].analyzers, 'trade_analyzer', None)
        
        # Check that no trades were made
        # This is a bit tricky because if no trades are made, the analysis might not have a 'total' attribute
        if trade_analyzer:
            analysis = trade_analyzer.get_analysis()
            assert not hasattr(analysis, 'total') or analysis.total.total == 0, "Trades were made when volume confirmation should have failed"
    
    def test_strategy_parameters(self):
        """Test that the strategy parameters can be configured."""
        # Custom parameters
        params = {
            'lookback': 30,
            'volume_ma_period': 15,
            'volume_mult': 2.0,
            'atr_period': 10,
            'initial_stop_atr_mult': 1.5,
            'trail_stop_atr_mult': 2.5
        }
        
        # Suppress logging during tests
        with patch('logging.Logger.info'):
            results = self.run_backtest('breakout', params)
        
        # Get the strategy instance
        strategy = results[0]
        
        # Check that parameters were passed correctly
        assert strategy.params.lookback == 30
        assert strategy.params.volume_ma_period == 15
        assert strategy.params.volume_mult == 2.0
        assert strategy.params.atr_period == 10
        assert strategy.params.initial_stop_atr_mult == 1.5
        assert strategy.params.trail_stop_atr_mult == 2.5
