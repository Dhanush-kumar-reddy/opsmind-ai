from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database.connection import Base


class IncidentMemory(Base):

    __tablename__ = "incident_memory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(String)

    service = Column(String)

    severity = Column(String)

    description = Column(Text)

    root_cause = Column(Text)

    recommended_fix = Column(Text)

    confidence = Column(String)