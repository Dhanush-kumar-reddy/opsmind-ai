import pandas as pd
import streamlit as st
import requests
from app.graph.workflow import graph

from app.database.incident_memory import (
    get_all_incidents
)

from app.tools.metrics_tool import (
    load_metrics
)


st.set_page_config(
    page_title="OpsMind AI",
    layout="wide"
)

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
        ["Low", "Medium", "High"]
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

    incident = {
        "incident_id": "LIVE_INCIDENT",
        "service": service,
        "severity": severity,
        "description": description
    }

    with st.spinner(
        "Running multi-agent analysis..."
    ):

        response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json=incident
    )

    result = response.json()

    summary = result["summary_result"]

    st.success(
        "Incident analysis completed."
    )

    tabs = st.tabs([
        "Overview",
        "Logs",
        "Metrics",
        "History",
        "Workflow"
    ])

    with tabs[0]:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Incident")

            st.write(
                f"Service: {summary['service']}"
            )

            st.write(
                f"Severity: {summary['severity']}"
            )

            st.write(
                f"Description: "
                f"{summary['description']}"
            )

        with col2:

            st.subheader("Analysis")

            st.write(
                f"Root Cause: "
                f"{summary['root_cause']}"
            )

            st.write(
                f"Impact: "
                f"{summary['impact']}"
            )

            st.write(
                f"Confidence: "
                f"{summary['confidence']}"
            )

        st.subheader("Recommended Fix")

        st.info(
            summary["recommended_fix"]
        )

    with tabs[1]:

        st.subheader("Retrieved Logs")

        logs = result["retrieval_result"][
            "relevant_logs"
        ]

        for log in logs:

            st.markdown(
                f"### {log['file']}"
            )

            for entry in log["entries"]:

                st.code(entry)

    with tabs[2]:

        st.subheader(
            "System Metrics"
        )

        metrics_data = load_metrics()

        for metric in metrics_data:

            st.markdown(
                f"## {metric['service']}"
            )

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            with col1:

                st.metric(
                    "CPU %",
                    metric["cpu_usage"]
                )

            with col2:

                st.metric(
                    "Memory %",
                    metric["memory_usage"]
                )

            with col3:

                st.metric(
                    "Error Rate %",
                    metric["error_rate"]
                )

            with col4:

                healthy = (
                    f"{metric['healthy_instances']}"
                    f"/"
                    f"{metric['total_instances']}"
                )

                st.metric(
                    "Healthy Instances",
                    healthy
                )

            chart_data = {
                "CPU": metric["cpu_usage"],
                "Memory": (
                    metric["memory_usage"]
                ),
                "Error Rate": (
                    metric["error_rate"]
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

        st.success(
            "Retrieval Agent Completed"
        )

        st.success(
            "Log Analysis Agent Completed"
        )

        st.success(
            "Metrics Agent Completed"
        )

        st.success(
            "Root Cause Agent Completed"
        )

        st.success(
            "Summary Agent Completed"
        )