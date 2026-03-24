import pandas as pd
import numpy as np

class ExecutionSimulator:
    def __init__(self, initial_capital=100000.0):
        self.capital = initial_capital
        self.brokerage_rate = 0.0005 
        self.slippage_rate = 0.0003   
        self.stcg_tax = 0.15          

    def calculate_net_return(self, entry_price: float, exit_price: float, quantity: int) -> dict:
        """
        Calculates true profit after 'Real-World' frictions.
        """
        gross_profit = (exit_price - entry_price) * quantity
        
        # Frictions
        total_buy_value = entry_price * quantity
        total_sell_value = exit_price * quantity
        
        transaction_costs = (total_buy_value + total_sell_value) * (self.brokerage_rate + self.slippage_rate)
        taxable_profit = max(0, gross_profit - transaction_costs)
        tax_deduction = taxable_profit * self.stcg_tax
        
        net_profit = gross_profit - transaction_costs - tax_deduction
        roi_percent = (net_profit / total_buy_value) * 100

        return {
            "gross_profit": round(gross_profit, 2),
            "frictions": round(transaction_costs, 2),
            "tax": round(tax_deduction, 2),
            "net_profit": round(net_profit, 2),
            "roi_percent": round(roi_percent, 2)
        }

    def simulate_behavioral_efficiency(self, signal_accuracy: float, manual_accuracy: float = 0.45):
        """
        Quantifies 'Behavioral Efficiency' - the value of removing 'Gut Feel'[cite: 75, 115].
        """
        efficiency_gain = (signal_accuracy - manual_accuracy) * 100
        return f"Behavioral Edge: +{round(efficiency_gain, 2)}% decision accuracy improvement."