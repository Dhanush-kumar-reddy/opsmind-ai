import traceback

from fastapi import FastAPI

from app.graph.workflow import graph

from app.models.incident_models import (
    IncidentRequest
)

app = FastAPI()


@app.get("/")
def health_check():

    return {
        "status": "healthy",
        "service": "OpsMind AI"
    }


@app.post("/analyze")
def analyze_incident(
    incident: IncidentRequest
):

    try:

        result = graph.invoke({
            "incident": incident.dict()
        })

        return result

    except Exception:

        traceback.print_exc()

        return {
            "summary_result": {
                "incident_id": incident.incident_id,
                "service": incident.service,
                "severity": incident.severity,
                "description": incident.description,
                "errors_detected": 0,
                "warnings_detected": 0,
                "root_cause": "Unknown",
                "impact": "Unknown",
                "recommended_fix": (
                    "Check backend logs"
                ),
                "confidence": "low",
                "status": "failed"
            },
            "retrieval_result": {
                "relevant_logs": [],
                "relevant_docs": []
            }
        }