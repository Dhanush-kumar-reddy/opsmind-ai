import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
    
import time
import graphviz

import pandas as pd
import requests
import streamlit as st

from app.database.incident_memory import (
    get_all_incidents
)

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


st.set_page_config(
    page_title="OpsMind AI",
    layout="wide"
)

st.title("OpsMind AI")

st.subheader(
    "AI Incident Management System"
)


if "analysis_complete" not in st.session_state:

    st.session_state.analysis_complete = False


if "result" not in st.session_state:

    st.session_state.result = None


if "workflow_steps" not in st.session_state:

    st.session_state.workflow_steps = []


if "agent_timings" not in st.session_state:

    st.session_state.agent_timings = {}


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

    st.session_state.analysis_complete = False

    st.session_state.result = None

    st.session_state.workflow_steps = []

    st.session_state.agent_timings = {}

    incident = {
        "incident_id": "LIVE_INCIDENT",
        "service": service,
        "severity": severity,
        "description": description
    }

    workflow_container = st.container()

    try:

        overall_start = time.time()

        with workflow_container:

            st.subheader(
                "Multi-Agent Execution"
            )

            retrieval_status = st.empty()

            log_status = st.empty()

            metrics_status = st.empty()

            root_status = st.empty()

            summary_status = st.empty()

            retrieval_start = time.time()

            retrieval_status.info(
                "Retrieval Agent Running..."
            )

            time.sleep(0.5)

            retrieval_time = round(
                time.time() - retrieval_start,
                2
            )

            retrieval_status.success(
                f"Retrieval Agent Completed "
                f"({retrieval_time}s)"
            )

            st.session_state.workflow_steps.append(
                "Retrieval Agent Completed"
            )

            st.session_state.agent_timings[
                "Retrieval Agent"
            ] = retrieval_time

            log_start = time.time()

            log_status.info(
                "Log Analysis Agent Running..."
            )

            time.sleep(0.5)

            log_time = round(
                time.time() - log_start,
                2
            )

            log_status.success(
                f"Log Analysis Agent Completed "
                f"({log_time}s)"
            )

            st.session_state.workflow_steps.append(
                "Log Analysis Agent Completed"
            )

            st.session_state.agent_timings[
                "Log Analysis Agent"
            ] = log_time

            metrics_start = time.time()

            metrics_status.info(
                "Metrics Agent Running..."
            )

            time.sleep(0.5)

            metrics_time = round(
                time.time() - metrics_start,
                2
            )

            metrics_status.success(
                f"Metrics Agent Completed "
                f"({metrics_time}s)"
            )

            st.session_state.workflow_steps.append(
                "Metrics Agent Completed"
            )

            st.session_state.agent_timings[
                "Metrics Agent"
            ] = metrics_time

            root_start = time.time()

            root_status.info(
                "Root Cause Agent Running..."
            )

            time.sleep(0.5)

            root_time = round(
                time.time() - root_start,
                2
            )

            root_status.success(
                f"Root Cause Agent Completed "
                f"({root_time}s)"
            )

            st.session_state.workflow_steps.append(
                "Root Cause Agent Completed"
            )

            st.session_state.agent_timings[
                "Root Cause Agent"
            ] = root_time

            summary_start = time.time()

            summary_status.info(
                "Summary Agent Running..."
            )

            with st.spinner(
                "Running multi-agent analysis..."
            ):

                response = requests.post(
                    API_URL,
                    json=incident,
                    timeout=API_TIMEOUT
                )

            if response.status_code != 200:

                summary_status.error(
                    "Summary Agent Failed"
                )

                st.error(
                    f"Backend Error: "
                    f"{response.text}"
                )

                st.stop()

            try:

                result = response.json()

            except Exception:

                summary_status.error(
                    "Invalid JSON Response"
                )

                st.error(
                    "Backend returned "
                    "invalid JSON response"
                )

                st.stop()

            if not isinstance(result, dict):

                summary_status.error(
                    "Malformed Response"
                )

                st.error(
                    "Backend returned "
                    "unexpected response format"
                )

                st.stop()

            if "summary_result" not in result:

                summary_status.error(
                    "Missing Summary"
                )

                st.error(
                    "summary_result missing "
                    "from backend response"
                )

                st.json(result)

                st.stop()

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
            "Request timed out."
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

        st.subheader("Recommended Fix")

        st.info(
            summary.get(
                "recommended_fix",
                "No recommendation"
            )
        )

    with tabs[1]:

        st.subheader("Retrieved Logs")

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

        st.subheader(
            "Log Summary"
        )

        col1, col2, col3 = st.columns(3)

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

        if total_errors >= 4:

            st.error(
                "Critical operational issue detected."
            )

        elif total_warnings >= 3:

            st.warning(
                "System instability detected."
            )

        else:

            st.success(
                "System appears stable."
            )

    with tabs[2]:

        st.subheader(
            "System Metrics"
        )

        metrics_data = load_metrics()

        for metric in metrics_data:

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

            chart_data = {
                "CPU": metric.get(
                    "cpu_usage",
                    0
                ),
                "Memory": metric.get(
                    "memory_usage",
                    0
                ),
                "Error Rate": metric.get(
                    "error_rate",
                    0
                )
            }

            st.bar_chart(chart_data)

            st.divider()

    with tabs[3]:

        st.subheader(
            "Historical Incidents"
        )

        incidents = get_all_incidents()

        rows = []

        for incident in incidents:

            rows.append({
                "Incident ID": (
                    incident.incident_id
                ),
                "Service": incident.service,
                "Severity": incident.severity,
                "Root Cause": (
                    incident.root_cause
                ),
                "Confidence": (
                    incident.confidence
                )
            })

        dataframe = pd.DataFrame(rows)

        st.dataframe(
            dataframe,
            use_container_width=True
        )

    with tabs[4]:

        st.subheader(
            "Workflow Execution"
        )

        timings = (
            st.session_state.agent_timings
        )

        for step in (
            st.session_state.workflow_steps
        ):

            st.success(step)

        st.divider()

        st.subheader(
            "Execution Timings"
        )

        rows = []

        for agent, timing in (
            timings.items()
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

        if timings:

            slowest_agent = max(
                timings,
                key=timings.get
            )

            st.warning(
                f"Slowest Step: "
                f"{slowest_agent}"
            )

        st.divider()

        st.subheader(
            "Agent Workflow Graph"
        )

        workflow_graph = graphviz.Digraph()

        workflow_graph.node(
            "Retrieval",
            "Retrieval Agent"
        )

        workflow_graph.node(
            "Logs",
            "Log Analysis Agent"
        )

        workflow_graph.node(
            "Metrics",
            "Metrics Agent"
        )

        workflow_graph.node(
            "Root",
            "Root Cause Agent"
        )

        workflow_graph.node(
            "Summary",
            "Summary Agent"
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