from datetime import datetime


def generate_incident_summary(
    incident: dict,
    log_analysis: dict,
    root_cause_result: dict
):

    analysis = root_cause_result.get(
        "root_cause_analysis",
        {}
    )

    errors = log_analysis.get(
        "errors",
        []
    )

    warnings = log_analysis.get(
        "warnings",
        []
    )

    severity = incident.get(
        "severity",
        "Low"
    )

    if severity == "High":

        priority = "P1"

    elif severity == "Medium":

        priority = "P2"

    else:

        priority = "P3"

    if len(errors) >= 5:

        health_status = (
            "Critical System Failure"
        )

    elif len(errors) >= 2:

        health_status = (
            "System Degraded"
        )

    else:

        health_status = (
            "System Stable"
        )

    summary = {
        "incident_id": incident.get(
            "incident_id",
            "UNKNOWN"
        ),

        "timestamp": str(
            datetime.utcnow()
        ),

        "service": incident.get(
            "service",
            "Unknown Service"
        ),

        "severity": severity,

        "priority": priority,

        "description": incident.get(
            "description",
            "No description provided"
        ),

        "errors_detected": len(errors),

        "warnings_detected": len(
            warnings
        ),

        "health_status": health_status,

        "root_cause": analysis.get(
            "root_cause",
            "Root cause not identified"
        ),

        "impact": analysis.get(
            "impact",
            "Impact unknown"
        ),

        "recommended_fix": analysis.get(
            "recommended_fix",
            "No recommendation available"
        ),

        "confidence": analysis.get(
            "confidence",
            "low"
        ),

        "status": (
            "investigation_completed"
        )
    }

    return summary