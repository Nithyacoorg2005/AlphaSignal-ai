from langgraph.graph import StateGraph, END
from agents.signal_finder import SignalFinder
from agents.risk_agent import RiskAgent
from agents.portfolio_agent import PortfolioAgent
from simulators.execution_sim import ExecutionSimulator


signal_finder = SignalFinder()
risk_evaluator = RiskAgent()
portfolio_manager = PortfolioAgent()
executor = ExecutionSimulator()


def detect_signal_node(state):
    result = signal_finder.find(state["ticker"])
    return {
        **state, 
        "signal_data": result["data"],
        "sources": result["sources"],
        "decision_graph": state["decision_graph"] + ["Signal: Data delta detected."]
    }

def risk_veto_node(state):
    result = risk_evaluator.evaluate(state)
    return {
        **state, 
        "is_vetoed": result["is_vetoed"],
        "risk_assessment": result["risk_assessment"],
        "decision_graph": result["decision_graph"]
    }

def portfolio_impact_node(state):
    
    result = portfolio_manager.analyze_impact(state)
    return {
        **state, 
        "portfolio_impact_results": result["portfolio_impact"],
        "decision_graph": result["decision_graph"]
    }
    

workflow = StateGraph(dict) 

workflow.add_node("signal", detect_signal_node)
workflow.add_node("risk", risk_veto_node)
workflow.add_node("portfolio", portfolio_impact_node)

workflow.set_entry_point("signal")
workflow.add_edge("signal", "risk")


workflow.add_conditional_edges(
    "risk",
    lambda x: "end" if x["is_vetoed"] else "portfolio",
    {
        "end": END,
        "portfolio": "portfolio"
    }
)

workflow.add_edge("portfolio", END)

app = workflow.compile()