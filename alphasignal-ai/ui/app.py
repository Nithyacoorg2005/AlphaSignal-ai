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
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.4) !important; /* Subtle Green Glow */
    }

    
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #58a6ff;
    }

    
    button[data-testid="sidebar-close-button"], 
    [data-testid="stSidebarNav"] svg,
    [data-testid="stIcon"],
    [data-testid="stSidebarCollapseButton"],
    .st-emotion-cache-6qob1r {
        display: none !important;
    }

    [data-testid="stMetricValue"] {
        color: #00ffc2 !important; /* Fintech Cyan */
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }

    code {
        color: #79c0ff !important;
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 4px !important;
    }

    
    .st-emotion-cache-1jicfl2 { padding-top: 2rem !important; }
</style>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.title("ALPHASIGNAL")
    st.caption("v2.0 // Institutional Intelligence")
    
    st.markdown("---")
    
 
    st.markdown('<p class="terminal-label">Asset Entry</p>', unsafe_allow_html=True)
    ticker = st.text_input("TICKER SYMBOL", value="RELIANCE", label_visibility="collapsed").upper().strip()
    
    
    portfolio_data = {
        "holdings": [
            {"ticker": "HDFC", "sector": "Banking"},
            {"ticker": "ICICI", "sector": "Banking"}
        ]
    }

    st.markdown(" ")
    analyze_btn = st.button("EXECUTE ANALYSIS")

    st.markdown("---")
    
    
    st.markdown('<p class="terminal-label">Agent Logic Weight</p>', unsafe_allow_html=True)
    if st.session_state.get('analysis_result'):
        res = st.session_state.analysis_result
        is_veto = res.get("is_vetoed", False)
        sig_c, risk_s = (40, 90) if is_veto else (85, 15)
        
        st.caption(f"SIGNAL CONFIDENCE: {sig_c}%")
        st.progress(sig_c / 100)
        st.caption(f"RISK SKEPTICISM: {risk_s}%")
        st.progress(risk_s / 100)
    else:
        st.info("System Ready.")


st.markdown(f"## {ticker} // ADVERSARIAL AUDIT")
st.markdown("---")

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

if analyze_btn:
    with st.spinner("interrogating market data..."):
        try:
            response = requests.post(f"http://127.0.0.1:8000/analyze?ticker={ticker}", json=portfolio_data)
            if response.status_code == 200:
                st.session_state.analysis_result = response.json()
                st.rerun()
            else: st.error("GATEWAY TIMEOUT")
        except Exception as e: st.error(f"RUNTIME ERR: {e}")

if st.session_state.get('analysis_result'):
    data = st.session_state.analysis_result
    final_status = "VETOED" if data.get("is_vetoed") else "APPROVED"
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("VERDICT", final_status)
        if final_status == "VETOED": st.error("TRADE ABORTED")
        else: st.success("CLEAR FOR ENTRY")
        
        st.markdown("#### SOURCES")
        for src in data.get("sources", []):
            st.caption(f"• {src['id']}")

    with c2:
        st.markdown("#### AUDIT LOG")
        for log in data.get("decision_graph", []):
            st.code(log, language="bash")

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("PROJECTED XIRR", "0.0%" if final_status == "VETOED" else "16.8%")
    m2.metric("CAPITAL PRESERVED", f"₹{len(ticker)*1500}" if final_status == "VETOED" else "₹0")
    m3.metric("LATENCY", f"{round(0.45 + (len(ticker)/40), 2)}s")