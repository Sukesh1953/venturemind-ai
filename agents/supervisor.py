from langgraph.graph import StateGraph, END

from models.state import VentureMindState

from agents.website_agent import website_agent
from agents.research_agent import research_agent
from agents.business_analysis_agent import business_analysis_agent
from agents.report_agent import report_agent


graph = StateGraph(VentureMindState)

# Nodes
graph.add_node("website", website_agent)
graph.add_node("research", research_agent)
graph.add_node("analysis", business_analysis_agent)
graph.add_node("report", report_agent)

# Entry point
graph.set_entry_point("website")

# Workflow
graph.add_edge("website", "research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", "report")
graph.add_edge("report", END)

# Compile
venturemind_graph = graph.compile()