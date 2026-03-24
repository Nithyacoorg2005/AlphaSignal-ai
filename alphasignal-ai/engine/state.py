from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    ticker: str
    portfolio_context: dict
    signal_data: Optional[dict]     
    risk_assessment: Optional[dict] 
    is_vetoed: bool                
    decision_graph: List[str]        
    sources: List[dict]              