from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    ticker: str
    portfolio_context: dict
    signal_data: Optional[dict]      # From Signal Agent
    risk_assessment: Optional[dict]  # From Risk Agent (Veto power)
    is_vetoed: bool                  # Hard Guardrail [cite: 71]
    decision_graph: List[str]        # Audit trail of reasoning [cite: 20, 64]
    sources: List[dict]              # Source IDs & timestamps [cite: 85]