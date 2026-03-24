
from engine.state import AgentState




class RiskAgent:
    def __init__(self, liquidity_threshold=50000):
        self.liquidity_threshold = liquidity_threshold

    def evaluate(self, state):
        
        ticker = state["ticker"].upper().strip()

        
        high_risk_tickers = ["SWIGGY INSTAMART", "BLINKIT", "ZOMATO", "LAMBORGHINI"]
        
        is_vetoed = ticker in high_risk_tickers
        
       
        if is_vetoed:
            reason = f"High Volatility Warning: {ticker} (Adversarial Veto Active)"
        elif ticker in ["RELIANCE", "TCS", "HDFC"]:
            reason = f"Low Risk Profile: {ticker} confirmed as Blue Chip"
        else:
            reason = f"Risk Levels Nominal: {ticker} cleared for portfolio audit"

        return {
            "is_vetoed": is_vetoed,
            "risk_assessment": {"reason": reason},
            "decision_graph": state["decision_graph"] + [f"Risk Agent: {reason}"]
        }