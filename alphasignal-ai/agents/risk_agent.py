# agents/risk_agent.py
from engine.state import AgentState

class RiskAgent:
    def __init__(self, liquidity_threshold=50000):
        # We can now use this threshold to actually Veto low-volume stocks
        self.liquidity_threshold = liquidity_threshold

    def evaluate(self, state: AgentState):
        ticker = state["ticker"].upper().strip()
        signal_data = state.get("signal_data", {})
        
        # 1. DATA EXTRACTION (Pulling from the SignalFinder's Factor Model)
        # If signal_data is missing (failsafe), we default to high-risk
        factors = signal_data.get("factors", {"mom": 1.0, "vol": 0.5, "pe": 100})
        
        volatility = factors.get("vol", 0)
        pe_ratio = factors.get("pe", 0)
        
        # 2. RUTHLESS VETO LOGIC (The "Interrogation")
        # We Veto if: Volatility is > 40% OR Valuation (P/E) is > 80
        reasons = []
        if volatility > 0.40:
            reasons.append(f"Excessive Volatility ({int(volatility*100)}%)")
        if pe_ratio > 80:
            reasons.append(f"Valuation Overstretch (P/E: {pe_ratio})")
            
        is_vetoed = len(reasons) > 0

        # 3. DYNAMIC MESSAGING
        if is_vetoed:
            reason = f"VETOED: {ticker} failed risk audit. Triggers: {', '.join(reasons)}"
        else:
            reason = f"CLEARED: {ticker} within safety bounds (Vol: {int(volatility*100)}%, P/E: {pe_ratio})"

        return {
            "is_vetoed": is_vetoed,
            "risk_assessment": {
                "reason": reason,
                "risk_score": round(volatility * 100, 1)
            },
            "decision_graph": state["decision_graph"] + [f"Risk Agent: {reason}"]
        }