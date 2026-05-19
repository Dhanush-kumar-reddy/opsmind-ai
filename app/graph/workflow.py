from app.database.incident_memory import (
    store_incident
)
from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.agents.retrieval_agent import retrieve_context
from app.agents.log_analysis_agent import analyze_logs
from app.agents.root_cause_agent import identify_root_cause
from app.agents.summary_agent import generate_incident_summary
from app.agents.metrics_agent import analyze_metrics


def retrieval_node(state: AgentState):

    retrieval_result = retrieve_context(
        state["incident"]
    )

    return {
        "retrieval_result": retrieval_result
    }


def analysis_node(state: AgentState):

    analysis_result = analyze_logs(
        state["retrieval_result"]["relevant_logs"]
    )

    return {
        "analysis_result": analysis_result
    }


def metrics_node(state: AgentState):

    metrics_result = analyze_metrics()

    return {
        "metrics_result": metrics_result
    }


def root_cause_node(state: AgentState):

    root_cause_result = identify_root_cause(
        incident=state["incident"],
        log_analysis=state["analysis_result"],
        retrieved_docs=state["retrieval_result"][
            "relevant_docs"
        ],
        metrics_result=state["metrics_result"]
    )

    return {
        "root_cause_result": root_cause_result
    }


def summary_node(state: AgentState):

    summary_result = generate_incident_summary(
        incident=state["incident"],
        log_analysis=state["analysis_result"],
        root_cause_result=state["root_cause_result"]
    )
    
    store_incident(summary_result)
    
    return {
        "summary_result": summary_result
    }


workflow = StateGraph(AgentState)

workflow.add_node(
    "retrieval_node",
    retrieval_node
)

workflow.add_node(
    "analysis_node",
    analysis_node
)

workflow.add_node(
    "metrics_node",
    metrics_node
)

workflow.add_node(
    "root_cause_node",
    root_cause_node
)

workflow.add_node(
    "summary_node",
    summary_node
)

workflow.set_entry_point(
    "retrieval_node"
)

workflow.add_edge(
    "retrieval_node",
    "analysis_node"
)

workflow.add_edge(
    "retrieval_node",
    "metrics_node"
)

workflow.add_edge(
    "analysis_node",
    "root_cause_node"
)

workflow.add_edge(
    "metrics_node",
    "root_cause_node"
)

workflow.add_edge(
    "root_cause_node",
    "summary_node"
)

workflow.add_edge(
    "summary_node",
    END
)

graph = workflow.compile()