import sys
import time
from pathlib import Path

import graphviz
import pandas as pd
import requests
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:

    sys.path.append(str(ROOT_DIR))

from app.tools.metrics_tool import (
    load_metrics
)

from app.rag.incident_similarity import (
    find_similar_incidents
)

from app.core.config import (
    API_TIMEOUT
)

API_URL = (
    "https://opsmind-ai-i2y2.onrender.com/analyze"
)


def get_status(severity):

    if severity == "High":

        return (
            "🔴 Critical",
            "error"
        )

    if severity == "Medium":

        return (
            "🟡 Investigating",
            "warning"
        )

    return (
        "🟢 Stable",
        "success"
    )


def initialize_session():

    defaults = {
        "analysis_complete": False,
        "result": None,
        "workflow_steps": [],
        "agent_timings": {}
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def reset_session():

    st.session_state.analysis_complete = False

    st.session_state.result = None

    st.session_state.workflow_steps = []

    st.session_state.agent_timings = {}


def execute_agent_step(
    status_container,
    agent_name
):

    start_time = time.time()

    status_container.info(
        f"{agent_name} Running..."
    )

    time.sleep(0.5)

    execution_time = round(
        time.time() - start_time,
        2
    )

    status_container.success(
        f"{agent_name} Completed "
        f"({execution_time}s)"
    )

    st.session_state.workflow_steps.append(
        f"{agent_name} Completed"
    )

    st.session_state.agent_timings[
        agent_name
    ] = execution_time


def call_backend_api(incident):

    response = requests.post(
        API_URL,
        json=incident,
        timeout=API_TIMEOUT
    )

    if response.status_code != 200:

        raise Exception(
            f"Backend Error: "
            f"{response.text}"
        )

    result = response.json()

    if not isinstance(result, dict):

        raise Exception(
            "Invalid backend response"
        )

    if "summary_result" not in result:

        raise Exception(
            "summary_result missing"
        )

    return result


st.set_page_config(
    page_title="OpsMind AI",
    layout="wide"
)

initialize_session()

st.title("OpsMind AI")

st.subheader(
    "AI Incident Management System"
)

with st.sidebar:

    st.header("Incident Input")

    service = st.text_input(
        "Service",
        value="Auth API"
    )

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High"],
        index=2
    )

    description = st.text_area(
        "Incident Description",
        value=(
            "Users unable to login "
            "after latest deployment"
        )
    )

    analyze_button = st.button(
        "Analyze Incident"
    )

if analyze_button:

    reset_session()

    incident = {
        "incident_id": "LIVE_INCIDENT",
        "service": service,
        "severity": severity,
        "description": description
    }

    try:

        overall_start = time.time()

        st.subheader(
            "Multi-Agent Execution"
        )

        retrieval_status = st.empty()

        log_status = st.empty()

        metrics_status = st.empty()

        root_status = st.empty()

        summary_status = st.empty()

        execute_agent_step(
            retrieval_status,
            "Retrieval Agent"
        )

        execute_agent_step(
            log_status,
            "Log Analysis Agent"
        )

        execute_agent_step(
            metrics_status,
            "Metrics Agent"
        )

        execute_agent_step(
            root_status,
            "Root Cause Agent"
        )

        summary_status.info(
            "Summary Agent Running..."
        )

        summary_start = time.time()

        with st.spinner(
            "Running multi-agent analysis..."
        ):

            result = call_backend_api(
                incident
            )

        summary_time = round(
            time.time() - summary_start,
            2
        )

        summary_status.success(
            f"Summary Agent Completed "
            f"({summary_time}s)"
        )

        st.session_state.workflow_steps.append(
            "Summary Agent Completed"
        )

        st.session_state.agent_timings[
            "Summary Agent"
        ] = summary_time

        total_time = round(
            time.time() - overall_start,
            2
        )

        st.session_state.agent_timings[
            "Total Execution"
        ] = total_time

        st.session_state.result = result

        st.session_state.analysis_complete = True

        st.success(
            f"Incident analysis completed "
            f"in {total_time}s"
        )

    except requests.exceptions.Timeout:

        st.error(
            "Backend request timed out."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to backend."
        )

    except Exception as error:

        st.error(
            f"Unexpected Error: {error}"
        )

if st.session_state.analysis_complete:

    result = st.session_state.result

    summary = result.get(
        "summary_result",
        {}
    )

    tabs = st.tabs([
        "Overview",
        "Logs",
        "Metrics",
        "History",
        "Workflow",
        "Similar Incidents"
    ])

    with tabs[0]:

        top_col1, top_col2, top_col3 = (
            st.columns(3)
        )

        with top_col1:

            st.metric(
                "Errors",
                summary.get(
                    "errors_detected",
                    0
                )
            )

        with top_col2:

            st.metric(
                "Warnings",
                summary.get(
                    "warnings_detected",
                    0
                )
            )

        with top_col3:

            st.metric(
                "Confidence",
                summary.get(
                    "confidence",
                    "low"
                )
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Incident")

            st.write(
                f"Service: "
                f"{summary.get('service', 'Unknown')}"
            )

            st.write(
                f"Severity: "
                f"{summary.get('severity', 'Unknown')}"
            )

            status_text, status_type = (
                get_status(
                    summary.get(
                        "severity",
                        "Low"
                    )
                )
            )

            if status_type == "error":

                st.error(status_text)

            elif status_type == "warning":

                st.warning(status_text)

            else:

                st.success(status_text)

            st.write(
                f"Description: "
                f"{summary.get('description', 'No description')}"
            )

        with col2:

            st.subheader("Analysis")

            st.write(
                f"Root Cause: "
                f"{summary.get('root_cause', 'Unknown')}"
            )

            st.write(
                f"Impact: "
                f"{summary.get('impact', 'Unknown')}"
            )

            st.write(
                f"Confidence: "
                f"{summary.get('confidence', 'low')}"
            )

        st.subheader(
            "Recommended Fix"
        )

        st.info(
            summary.get(
                "recommended_fix",
                "No recommendation"
            )
        )

    with tabs[1]:

        st.subheader(
            "Retrieved Logs"
        )

        logs = (
            result.get(
                "retrieval_result",
                {}
            ).get(
                "relevant_logs",
                []
            )
        )

        total_errors = 0
        total_warnings = 0
        total_info = 0

        if not logs:

            st.info(
                "No logs retrieved."
            )

        else:

            for log in logs:

                st.markdown(
                    f"### "
                    f"{log.get('file', 'Unknown File')}"
                )

                entries = log.get(
                    "entries",
                    []
                )

                for entry in entries:

                    if "ERROR" in entry:

                        total_errors += 1

                        st.error(
                            f"🔴 {entry}"
                        )

                    elif "WARNING" in entry:

                        total_warnings += 1

                        st.warning(
                            f"🟡 {entry}"
                        )

                    else:

                        total_info += 1

                        st.info(
                            f"🔵 {entry}"
                        )

        st.divider()

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:

            st.metric(
                "Errors",
                total_errors
            )

        with col2:

            st.metric(
                "Warnings",
                total_warnings
            )

        with col3:

            st.metric(
                "Info Logs",
                total_info
            )

    with tabs[2]:

        st.subheader(
            "System Metrics"
        )

        metrics_data = load_metrics()

        if not metrics_data:

            st.warning(
                "No metrics data found."
            )

        else:

            for metric in metrics_data:

                if not isinstance(
                    metric,
                    dict
                ):

                    continue

                st.markdown(
                    f"## "
                    f"{metric.get('service', 'Unknown')}"
                )

                col1, col2, col3, col4 = (
                    st.columns(4)
                )

                with col1:

                    st.metric(
                        "CPU %",
                        metric.get(
                            "cpu_usage",
                            0
                        )
                    )

                with col2:

                    st.metric(
                        "Memory %",
                        metric.get(
                            "memory_usage",
                            0
                        )
                    )

                with col3:

                    st.metric(
                        "Error Rate %",
                        metric.get(
                            "error_rate",
                            0
                        )
                    )

                with col4:

                    healthy = (
                        f"{metric.get('healthy_instances', 0)}"
                        f"/"
                        f"{metric.get('total_instances', 0)}"
                    )

                    st.metric(
                        "Healthy Instances",
                        healthy
                    )

                chart_data = pd.DataFrame({
                    "Metric": [
                        "CPU",
                        "Memory",
                        "Error Rate"
                    ],
                    "Value": [
                        metric.get(
                            "cpu_usage",
                            0
                        ),
                        metric.get(
                            "memory_usage",
                            0
                        ),
                        metric.get(
                            "error_rate",
                            0
                        )
                    ]
                })

                st.bar_chart(
                    chart_data.set_index(
                        "Metric"
                    )
                )

                st.divider()

    with tabs[3]:

        st.subheader(
            "Historical Incidents"
        )

        st.info(
            "Historical incidents are "
            "managed by backend services."
        )

    with tabs[4]:

        st.subheader(
            "Workflow Execution"
        )

        for step in (
            st.session_state.workflow_steps
        ):

            st.success(step)

        st.divider()

        rows = []

        for agent, timing in (
            st.session_state.agent_timings.items()
        ):

            rows.append({
                "Agent": agent,
                "Execution Time (s)": timing
            })

        timing_df = pd.DataFrame(rows)

        st.dataframe(
            timing_df,
            use_container_width=True
        )

        workflow_graph = graphviz.Digraph()

        workflow_graph.node(
            "Retrieval"
        )

        workflow_graph.node(
            "Logs"
        )

        workflow_graph.node(
            "Metrics"
        )

        workflow_graph.node(
            "Root"
        )

        workflow_graph.node(
            "Summary"
        )

        workflow_graph.edge(
            "Retrieval",
            "Logs"
        )

        workflow_graph.edge(
            "Retrieval",
            "Metrics"
        )

        workflow_graph.edge(
            "Logs",
            "Root"
        )

        workflow_graph.edge(
            "Metrics",
            "Root"
        )

        workflow_graph.edge(
            "Root",
            "Summary"
        )

        st.graphviz_chart(
            workflow_graph
        )

    with tabs[5]:

        st.subheader(
            "Similar Historical Incidents"
        )

        try:

            similar_incidents = (
                find_similar_incidents(
                    summary.get(
                        "description",
                        ""
                    )
                )
            )

            if not similar_incidents:

                st.info(
                    "No similar incidents found."
                )

            else:

                for incident in similar_incidents:

                    metadata = getattr(
                        incident,
                        "metadata",
                        {}
                    )

                    st.markdown(
                        f"### "
                        f"{metadata.get('incident_id', 'Unknown')}"
                    )

                    st.write(
                        f"Service: "
                        f"{metadata.get('service', 'Unknown')}"
                    )

                    st.write(
                        f"Root Cause: "
                        f"{metadata.get('root_cause', 'Unknown')}"
                    )

                    st.code(
                        incident.page_content
                    )

                    st.divider()

        except Exception as error:

            st.error(
                f"Similarity Search Error: "
                f"{error}"
            )