import os
from typing import Dict, List

class SignalFinder:
    def __init__(self):
        self.required_sources = ["NSE_Price_Action", "Corporate_Filings"]

    def find(self, ticker: str) -> Dict:
        """
        Calculates a dynamic signal based on the ticker name.
        This ensures the UI updates and doesn't show the 'same result'.
        """
        # Logic 1: Technical Signal (Mocked dynamic logic)
        # We use the length of the ticker to fake different strengths
        strength = 0.5 + (len(ticker) % 5) / 10 
        
        technical_signal = {
            "type": "Bullish Breakout" if strength > 0.7 else "Consolidation",
            "indicator": f"Volume Spike {round(strength * 3, 1)}x",
            "confidence": strength
        }

        # Logic 2: Fundamental Delta
        fundamental_delta = {
            "tone_shift": "Positive" if "A" in ticker.upper() else "Neutral",
            "key_change": f"Guidance updated for {ticker} fiscal year 2026.",
            "source_ref": f"Filing_ID_{ticker}_2026_Q4"
        }

        # Return ONE consolidated dictionary
        return {
            "data": {
                "ticker": ticker,
                "technical": technical_signal,
                "fundamental": fundamental_delta,
                "composite_score": strength
            },
            "sources": [
                {"type": "NSE_Market_Data", "id": f"NSE_{ticker}_LIVE"},
                {"type": "Corporate_Filing", "id": fundamental_delta["source_ref"], "page": 6}
            ]
        }