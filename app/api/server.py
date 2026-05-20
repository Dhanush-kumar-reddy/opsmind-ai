import traceback
from fastapi import FastAPI

from app.graph.workflow import graph

app = FastAPI()


@app.post("/analyze")
def analyze_incident(incident: dict):

    try:

        result = graph.invoke({
            "incident": incident
        })

        return result

    except Exception as error:

        traceback.print_exc()

        return {
            "summary_result": {
                "incident_id": incident.get(
                    "incident_id",
                    "UNKNOWN"
                ),
                "service": incident.get(
                    "service",
                    "Unknown Service"
                ),
                "severity": incident.get(
                    "severity",
                    "Low"
                ),
                "description": incident.get(
                    "description",
                    "No description provided"
                ),
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