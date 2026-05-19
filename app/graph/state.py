from typing import TypedDict


class AgentState(TypedDict):
    incident: dict
    retrieval_result: dict
    analysis_result: dict
    metrics_result: dict
    root_cause_result: dict
    summary_result: dict