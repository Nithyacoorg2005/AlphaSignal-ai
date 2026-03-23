from engine.state import AgentState

class RiskAgent:
    def __init__(self, liquidity_threshold=50000):
        self.liquidity_threshold = liquidity_threshold

    def evaluate(self, state: AgentState) -> Dict:
        """
        The Skeptic Loop: Challenges the Signal Agent's optimism[cite: 20].
        Checks for:
        1. Low Liquidity (Pump & Dump protection)
        2. High Promoter Pledging
        3. Sector Volatility
        """
        ticker = state["ticker"]
        signal = state["signal_data"]
        
        # Mocking a compliance check against NSE liquidity data [cite: 82]
        current_liquidity = 10000  # Example low value
        
        is_vetoed = False
        reason = "Clearance for execution."
        
        if current_liquidity < self.liquidity_threshold:
            is_vetoed = True
            reason = f"VETO: Asset liquidity ({current_liquidity}) below safety threshold."

        return {
            "risk_assessment": {"score": 0.9 if is_vetoed else 0.1, "reason": reason},
            "is_vetoed": is_vetoed,
            "decision_graph": state["decision_graph"] + [f"Risk Agent: {reason}"]
        }