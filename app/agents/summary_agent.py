def generate_incident_summary(
    incident: dict,
    log_analysis: dict,
    root_cause_result: dict
):

    analysis = root_cause_result[
        "root_cause_analysis"
    ]

    summary = {
        "incident_id": incident["incident_id"],
        "service": incident["service"],
        "severity": incident["severity"],
        "description": incident["description"],
        "errors_detected": len(
            log_analysis["errors"]
        ),
        "warnings_detected": len(
            log_analysis["warnings"]
        ),
        "root_cause": analysis["root_cause"],
        "impact": analysis["impact"],
        "recommended_fix": analysis[
            "recommended_fix"
        ],
        "confidence": analysis["confidence"],
        "status": "investigation_completed"
    }

    return summary