import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException


from agents.signal_finder import SignalFinder
from agents.risk_agent import RiskAgent

api = FastAPI(title="AlphaSignal AI - Institutional Gateway")


sig_engine = SignalFinder()
risk_engine = RiskAgent()


class Holding(BaseModel):
    ticker: str
    sector: str

class PortfolioData(BaseModel):
    holdings: List[Holding]

@api.get("/")
async def root():
    return {"status": "AlphaSignal Node Online", "version": "2.0"}

@api.post("/analyze")
async def run_analysis(ticker: str, portfolio: Optional[PortfolioData] = None):
    try:
       
        signal_result = sig_engine.find(ticker)
        
        if not signal_result:
            raise HTTPException(status_code=404, detail="Ticker data not found in market map")

        
        risk_result = risk_engine.evaluate(ticker, signal_result)
        
       
        return {
            "ticker": ticker,
            "is_vetoed": risk_result["is_vetoed"],
            "mu": signal_result["mu"],
            "alpha": signal_result["alpha"],
            "sharpe": signal_result["sharpe"],
            "factors": signal_result["factors"],
            "stress_tests": signal_result["stress_tests"], 
            "backtest": signal_result["backtest"],
            "sources": signal_result["sources"],
            "risk_assessment": {"reason": risk_result["reason"]},
            "reasoning": signal_result.get("reasoning", "Analysis complete."),
            "decision_graph": [
                f"ENTRY: Initializing State for {ticker}",
                f"SIGNAL_AGENT: Computed μ={signal_result['mu']}%",
                f"RISK_VETO: {risk_result['reason']}"
            ]
        }
    except Exception as e:
        
        print(f"CRITICAL ENGINE ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000)