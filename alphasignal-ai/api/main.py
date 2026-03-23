from fastapi import FastAPI
from engine.graph import app as signal_engine

api = FastAPI(title="AlphaSignal AI Backend")

# api/main.py

@api.post("/analyze")
async def run_analysis(ticker: str, portfolio: dict):
    # CRITICAL: Ensure 'ticker' here matches the 'ticker' in the argument
    initial_state = {
        "ticker": ticker, 
        "portfolio_context": portfolio,
        "decision_graph": [],
        "is_vetoed": False,
        "signal_data": None,
        "sources": []
    }
    # Force a fresh invocation
    final_state = signal_engine.invoke(initial_state)
    return final_state
    
    return {
        "ticker": ticker,
        "status": "VETOED" if final_state["is_vetoed"] else "APPROVED",
        "audit_trail": final_state["decision_graph"],
        "sources": final_state["sources"],
        "impact": final_state.get("portfolio_context")
    }