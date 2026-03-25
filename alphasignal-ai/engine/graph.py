from langgraph.graph import StateGraph, END
from engine.state import AgentState
from agents.signal_finder import SignalFinder
from agents.risk_agent import RiskAgent


signal_finder = SignalFinder()
risk_evaluator = RiskAgent()


def detect_signal_node(state: AgentState):
    ticker = state["ticker"]
    
    result = signal_finder.find(ticker)
    
    return {
        "signal_data": result, 
        "factors": result.get("factors", {}),
        "mu": result.get("mu", 0),
        "alpha": result.get("alpha", 0),
        "sharpe": result.get("sharpe", 0.42),
        "sources": result.get("sources", [])
    }


def risk_veto_node(state: AgentState):
   
    result = risk_evaluator.evaluate(state)
    
    return {
        "is_vetoed": result["is_vetoed"],
        "risk_assessment": result["risk_assessment"],
        "decision_graph": result["decision_graph"]
    }


workflow = StateGraph(AgentState) 

workflow.add_node("signal", detect_signal_node)
workflow.add_node("risk", risk_veto_node)

workflow.set_entry_point("signal")
workflow.add_edge("signal", "risk")


workflow.add_conditional_edges(
    "risk",
    
    lambda x: "end" if x["is_vetoed"] else "continue",
    {
        "end": END,
        "continue": END 
    }
)


app = workflow.compile()