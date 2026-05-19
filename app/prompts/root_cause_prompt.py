def build_root_cause_prompt(
    incident: str,
    error_logs: list,
    documents: list,
    metrics_findings: list,
    historical_incidents: list
):

    return f"""
You are an AI SRE incident analyst.

Analyze the operational incident.

Incident:
{incident}

Errors:
{error_logs}

Documents:
{documents}

Metrics:
{metrics_findings}

Historical Incidents:
{historical_incidents}

You MUST return ONLY valid JSON.

Do not add markdown.
Do not add explanations.
Do not use triple backticks.

Return format:

{{
    "root_cause": "...",
    "impact": "...",
    "recommended_fix": "...",
    "confidence": "low/medium/high"
}}
"""