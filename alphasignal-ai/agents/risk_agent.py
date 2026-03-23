# agents/risk_agent.py
from engine.state import AgentState

class RiskAgent:
    def __init__(self, liquidity_threshold=50000):
        self.liquidity_threshold = liquidity_threshold

    def evaluate(self, state: AgentState): # <--- MUST BE INDENTED
        # Ensure we handle case sensitivity
        ticker = state["ticker"].upper()

        # DYNAMIC LOGIC: Veto only if it's NOT Reliance
        is_vetoed = False if ticker == "RELIANCE" else True
        reason = "Safe Asset: Reliance Industries" if not is_vetoed else f"High Volatility Warning: {ticker}"
        
        return {
            "is_vetoed": is_vetoed,
            "risk_assessment": {"reason": reason},
            "decision_graph": state["decision_graph"] + [f"Risk Agent: {reason}"]
        }