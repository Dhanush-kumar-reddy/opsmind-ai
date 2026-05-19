from app.database.incident_memory import (
    retrieve_similar_incidents
)


def incident_history_tool():

    incidents = retrieve_similar_incidents()

    formatted_incidents = []

    for incident in incidents:

        formatted_incidents.append({
            "incident_id": incident.incident_id,
            "service": incident.service,
            "root_cause": incident.root_cause,
            "recommended_fix": (
                incident.recommended_fix
            ),
            "confidence": incident.confidence
        })

    return formatted_incidents