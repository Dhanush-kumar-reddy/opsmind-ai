from app.database.connection import (
    SessionLocal
)

from app.database.models import (
    IncidentMemory
)


def store_incident(summary: dict):

    db = SessionLocal()

    incident = IncidentMemory(
        incident_id=summary["incident_id"],
        service=summary["service"],
        severity=summary["severity"],
        description=summary["description"],
        root_cause=summary["root_cause"],
        recommended_fix=summary[
            "recommended_fix"
        ],
        confidence=summary["confidence"]
    )

    db.add(incident)

    db.commit()

    db.close()


def retrieve_similar_incidents():

    db = SessionLocal()

    incidents = (
        db.query(IncidentMemory)
        .order_by(IncidentMemory.id.desc())
        .limit(5)
        .all()
    )

    db.close()

    return incidents


def get_all_incidents():

    db = SessionLocal()

    incidents = (
        db.query(IncidentMemory)
        .order_by(IncidentMemory.id.desc())
        .all()
    )

    db.close()

    return incidents