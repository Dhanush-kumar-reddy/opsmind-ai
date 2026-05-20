from app.database.incident_memory import (
    store_incident
)

from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import (
    AgentState
)

from app.agents.retrieval_agent import (
    retrieve_context
)

from app.agents.log_analysis_agent import (
    analyze_logs
)

from app.agents.root_cause_agent import (
    identify_root_cause
)

from app.agents.summary_agent import (
    generate_incident_summary
)

from app.agents.metrics_agent import (
    analyze_metrics
)


def retrieval_node(state: AgentState):

    try:

        retrieval_result = retrieve_context(
            state["incident"]
        )

        if not retrieval_result:

            retrieval_result = {
                "relevant_logs": [],
                "relevant_docs": []
            }

        return {
            "retrieval_result": retrieval_result
        }

    except Exception as error:

        print(
            "RETRIEVAL ERROR:",
            str(error)
        )

        return {
            "retrieval_result": {
                "relevant_logs": [],
                "relevant_docs": []
            }
        }


def analysis_node(state: AgentState):

    try:

        relevant_logs = (
            state.get(
                "retrieval_result",
                {}
            ).get(
                "relevant_logs",
                []
            )
        )

        analysis_result = analyze_logs(
            relevant_logs
        )

        if not analysis_result:

            analysis_result = {
                "errors": [],
                "warnings": [],
                "info": [],
                "summary": (
                    "Analysis unavailable"
                )
            }

        return {
            "analysis_result": analysis_result
        }

    except Exception as error:

        print(
            "ANALYSIS ERROR:",
            str(error)
        )

        return {
            "analysis_result": {
                "errors": [],
                "warnings": [],
                "info": [],
                "summary": (
                    "Analysis failed"
                )
            }
        }


def metrics_node(state: AgentState):

    try:

        metrics_result = analyze_metrics()

        if not metrics_result:

            metrics_result = {
                "metrics_findings": []
            }

        return {
            "metrics_result": metrics_result
        }

    except Exception as error:

        print(
            "METRICS ERROR:",
            str(error)
        )

        return {
            "metrics_result": {
                "metrics_findings": []
            }
        }


def root_cause_node(state: AgentState):

    try:

        incident = state.get(
            "incident",
            {}
        )

        log_analysis = state.get(
            "analysis_result",
            {}
        )

        retrieved_docs = (
            state.get(
                "retrieval_result",
                {}
            ).get(
                "relevant_docs",
                []
            )
        )

        metrics_result = state.get(
            "metrics_result",
            {}
        )

        root_cause_result = (
            identify_root_cause(
                incident=incident,
                log_analysis=log_analysis,
                retrieved_docs=retrieved_docs,
                metrics_result=metrics_result
            )
        )

        if not root_cause_result:

            root_cause_result = {
                "root_cause_analysis": {
                    "root_cause": (
                        "Unknown"
                    ),
                    "impact": (
                        "Unknown"
                    ),
                    "recommended_fix": (
                        "Manual investigation required"
                    ),
                    "confidence": "low"
                }
            }

        return {
            "root_cause_result": (
                root_cause_result
            )
        }

    except Exception as error:

        print(
            "ROOT CAUSE ERROR:",
            str(error)
        )

        return {
            "root_cause_result": {
                "root_cause_analysis": {
                    "root_cause": (
                        "Unknown"
                    ),
                    "impact": (
                        "Unknown"
                    ),
                    "recommended_fix": (
                        "Check backend logs"
                    ),
                    "confidence": "low"
                }
            }
        }


def summary_node(state: AgentState):

    try:

        incident = state.get(
            "incident",
            {}
        )

        log_analysis = state.get(
            "analysis_result",
            {}
        )

        root_cause_result = state.get(
            "root_cause_result",
            {}
        )

        summary_result = (
            generate_incident_summary(
                incident=incident,
                log_analysis=log_analysis,
                root_cause_result=(
                    root_cause_result
                )
            )
        )

        if not summary_result:

            summary_result = {
                "incident_id": (
                    incident.get(
                        "incident_id",
                        "UNKNOWN"
                    )
                ),
                "service": (
                    incident.get(
                        "service",
                        "Unknown"
                    )
                ),
                "severity": (
                    incident.get(
                        "severity",
                        "Unknown"
                    )
                ),
                "description": (
                    incident.get(
                        "description",
                        ""
                    )
                ),
                "errors_detected": 0,
                "warnings_detected": 0,
                "root_cause": (
                    "Unknown"
                ),
                "impact": (
                    "Unknown"
                ),
                "recommended_fix": (
                    "Manual investigation required"
                ),
                "confidence": "low",
                "status": (
                    "partial_failure"
                )
            }

        try:

            store_incident(
                summary_result
            )

        except Exception as db_error:

            print(
                "DATABASE ERROR:",
                str(db_error)
            )

        return {
            "summary_result": (
                summary_result
            )
        }

    except Exception as error:

        print(
            "SUMMARY ERROR:",
            str(error)
        )

        incident = state.get(
            "incident",
            {}
        )

        return {
            "summary_result": {
                "incident_id": (
                    incident.get(
                        "incident_id",
                        "UNKNOWN"
                    )
                ),
                "service": (
                    incident.get(
                        "service",
                        "Unknown"
                    )
                ),
                "severity": (
                    incident.get(
                        "severity",
                        "Unknown"
                    )
                ),
                "description": (
                    incident.get(
                        "description",
                        ""
                    )
                ),
                "errors_detected": 0,
                "warnings_detected": 0,
                "root_cause": (
                    "Analysis failed"
                ),
                "impact": (
                    "Unknown"
                ),
                "recommended_fix": (
                    "Check backend logs"
                ),
                "confidence": "low",
                "status": (
                    "failure"
                )
            }
        }


workflow = StateGraph(
    AgentState
)

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