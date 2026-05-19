import json

from app.llm.groq_client import (
    generate_response
)

from app.prompts.root_cause_prompt import (
    build_root_cause_prompt
)

from app.tools.incident_history_tool import (
    incident_history_tool
)

def identify_root_cause(
    incident: dict,
    log_analysis: dict,
    retrieved_docs: list,
    metrics_result: dict
):
    
    historical_incidents = (
        incident_history_tool()
    )
    
    error_logs = [
        error["message"]
        for error in log_analysis["errors"]
    ]

    documents = [
        doc["content"]
        for doc in retrieved_docs
    ]

    metrics_findings = metrics_result[
        "metrics_findings"
    ]

    prompt = build_root_cause_prompt(
        historical_incidents=historical_incidents,
        incident=incident["description"],
        error_logs=error_logs,
        documents=documents,
        metrics_findings=metrics_findings
    )

    response = generate_response(prompt)

    parsed_response = safe_json_parse(
        response
    )

    return {
        "incident_id": incident["incident_id"],
        "root_cause_analysis": parsed_response
    }


def safe_json_parse(response: str):

    try:
        return json.loads(response)

    except Exception:

        return {
            "root_cause": "Parsing failure",
            "impact": response,
            "recommended_fix": (
                "Inspect model output manually."
            ),
            "confidence": "low"
        }