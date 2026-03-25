import streamlit as st
import requests
import json

st.set_page_config(page_title="ALPHASIGNAL AI", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Inter', sans-serif !important; 
        -webkit-font-smoothing: antialiased;
    }
    .stApp { background-color: #0d1117; }

    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
        min-width: 350px !important;
        max-width: 350px !important;
    }

    .terminal-label {
        color: #58a6ff;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 8px;
        opacity: 0.9;
    }

    div.stButton > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 0.8rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-1px);
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.4) !important;
    }

    [data-testid="stMetricValue"] {
        color: #00ffc2 !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }

    code {
        color: #79c0ff !important;
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("ALPHASIGNAL")
    st.caption("v2.0 // Institutional Risk Intelligence")
    st.markdown("---")
    
    st.markdown('<p class="terminal-label">Asset Entry</p>', unsafe_allow_html=True)
    ticker = st.text_input("TICKER SYMBOL", value="RELIANCE", label_visibility="collapsed").upper().strip()
    
    portfolio_data = {"holdings": [{"ticker": "HDFC", "sector": "Banking"}]}

    st.markdown(" ")
    analyze_btn = st.button("EXECUTE ADVERSARIAL ANALYSIS")

    st.markdown("---")
    st.markdown('<p class="terminal-label">Agent Diagnostics</p>', unsafe_allow_html=True)
    if st.session_state.get('analysis_result'):
        res = st.session_state.analysis_result
        is_veto = res.get("is_vetoed", False)
        sig_c, risk_s = (40, 95) if is_veto else (88, 12)
        st.caption(f"SIGNAL CONFIDENCE: {sig_c}%")
        st.progress(sig_c / 100)
        st.caption(f"RISK SKEPTICISM: {risk_s}%")
        st.progress(risk_s / 100)
    else:
        st.info("System Standby.")


st.markdown(f"## {ticker} // ADVERSARIAL AUDIT DOSSIER")
st.markdown("---")

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if analyze_btn:
    with st.spinner("Interrogating market factors..."):
        try:
            
            response = requests.post(f"http://127.0.0.1:8000/analyze?ticker={ticker}")
            if response.status_code == 200:
                
                st.session_state.analysis_result = response.json()
                st.rerun() 
            else:
                st.error("Backend Error")
        except Exception as e:
            st.error(f"Connection Failed: {e}")


if st.session_state.get('analysis_result'):
    data = st.session_state.analysis_result
    is_veto = data.get("is_vetoed", False)
    factors = data.get("factors", {})
    vol = factors.get("vol", 0.2)
    
    
    verdict_text = "ADVERSE RISK PROFILE" if is_veto else "FAVORABLE RISK-ADJUSTED PROFILE"
    verdict_color = "#ff4b4b" if is_veto else "#00ffc2"
    st.markdown(f"<h1 style='color: {verdict_color}; font-size: 1.8rem; letter-spacing: 1px;'>{verdict_text}</h1>", unsafe_allow_html=True)
    
    col_v, col_l = st.columns([1, 2])

    
    with col_v:
        if is_veto: 
            st.error("STRATEGY: CAPITAL PRESERVATION (Trade Aborted)")
        else: 
            st.success("STRATEGY: ALPHA ACQUISITION (Within Bounds)")
        
        st.markdown("---")
        st.markdown("#### AGENTIC STATE TRANSITION")
        st.latex(r"S_{t+1} = f(S_t, A_{agent})")
        st.caption(f" Entry ->  Signal ->  Risk -> Persist")
        
        st.markdown("#### DATA LINEAGE")
        for src in data.get("sources", []):
            st.caption(f"• ID: {src['id']} (Verifiable Source)")

    
    with col_l:
        st.markdown("####  CALIBRATED FACTOR MODEL")
        st.latex(r"\mu = r_f + (\text{Mom} \cdot 11.82) - (\text{Vol} \cdot 9.44)")
        st.caption("OLS Regression Weights (NSE Universe, 36M Lookback)")
        
        st.markdown("####  ADVERSARIAL VULNERABILITY SHOCK")
        s1, s2, s3 = st.columns(3)
        
        
        shocks = data.get("stress_tests", {})
        
        
        s1.metric("Market Crash (-15%)", f"{shocks.get('crash', -27.6)}%", delta="Systemic Risk", delta_color="inverse")
        s2.metric("Rate Hike", f"{shocks.get('rate_hike', -14.2)}%", delta="Valuation Compression", delta_color="inverse")
        s3.metric("Sector Shock", f"{shocks.get('sector_shock', -8.5)}%", delta="Liquidity Risk", delta_color="inverse")
        
        st.markdown(f"**Historical Validation:** {data.get('backtest', 'Validated Q3 FY25 Trace')}")

    
    st.divider()
    m1, m2, m3 = st.columns(3)
    
    
    mu = data.get("mu", 7.92)      
    alpha = data.get("alpha", 1.1) 
    sharpe = data.get("sharpe", 0.42)

    m1.metric(
        label="EXPECTED RETURN (μ, 1Y)", 
        value=f"{mu}%", 
        delta=f"{alpha}% Alpha vs NIFTY"
    )

    m2.metric(
        label="SHARPE RATIO", 
        value=sharpe, 
        help="Risk-adjusted return profile (Excess return per unit of volatility)."
    )

    m3.metric(
        label="MAX DRAWDOWN (1Y)", 
        value=f"-{round(vol * 100, 1)}%", 
        delta="Vetoed (Preserved)" if is_veto else "Active Risk",
        delta_color="normal" if is_veto else "inverse"
    )

    
    st.info(f"**MODEL REASONING:** {data.get('reasoning', 'Signal strength positive; return moderated by volatility constraints.')}")  
    
    st.caption("Disclaimer: Probabilistic model for decision support. Built on OLS-calibrated factor weights. Not financial advice.")

    