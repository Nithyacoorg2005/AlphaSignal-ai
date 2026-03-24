from engine.state import AgentState

class PortfolioAgent:
    def analyze_impact(self, state: AgentState) -> dict:
        """
        Checks if the new signal creates 'Sector Overcrowding'.
        Prevents 'Flying Blind' into over-exposure[cite: 75].
        """
        current_portfolio = state["portfolio_context"].get("holdings", [])
        new_ticker = state["ticker"]
        new_sector = "Banking"  
        
     
        sector_counts = {}
        for stock in current_portfolio:
            s = stock.get("sector", "Unknown")
            sector_counts[s] = sector_counts.get(s, 0) + 1
            
        current_concentration = sector_counts.get(new_sector, 0) / len(current_portfolio) if current_portfolio else 0
        
        risk_flag = False
        if current_concentration > 0.25: 
            risk_flag = True
            
        message = f"Portfolio analysis complete. Sector exposure: {round(current_concentration*100, 2)}%."
        if risk_flag:
            message += " WARNING: High sector concentration detected."

        return {
            "portfolio_impact": {
                "concentration_risk": risk_flag,
                "message": message
            },
            "decision_graph": state["decision_graph"] + [message]
        }