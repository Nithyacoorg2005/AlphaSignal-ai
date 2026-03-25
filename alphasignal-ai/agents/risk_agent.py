class RiskAgent:
    def evaluate(self, ticker, signal_data): # ✅ Added 'self'
        vol = signal_data['factors']['vol']
        pe = signal_data['factors']['pe']
        
        reasons = []
        if vol > 0.45: reasons.append(f"Excessive Volatility ({int(vol*100)}%)")
        if pe > 85: reasons.append(f"Valuation Overstretch (P/E: {pe})")
            
        is_vetoed = len(reasons) > 0
        status = "VETOED" if is_vetoed else "CLEARED"
        msg = f"{status}: {ticker}. Basis: {', '.join(reasons) if is_vetoed else 'Metrics within Safety Band'}"
        
        return {"is_vetoed": is_vetoed, "reason": msg}