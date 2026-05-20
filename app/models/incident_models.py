from pydantic import BaseModel


class IncidentRequest(BaseModel):

    incident_id: str
    service: str
    severity: str
    description: str


class SummaryResult(BaseModel):

    incident_id: str
    service: str
    severity: str
    description: str
    errors_detected: int
    warnings_detected: int
    root_cause: str
    impact: str
    recommended_fix: str
    confidence: str
    status: str