import json

from app.utils.file_utils import INCIDENTS_DIR


def load_incident(filename: str) -> dict:
    file_path = INCIDENTS_DIR / filename

    with open(file_path, "r") as file:
        incident = json.load(file)

    return incident


def load_all_incidents() -> list:
    incidents = []

    for file_path in INCIDENTS_DIR.glob("*.json"):
        with open(file_path, "r") as file:
            incidents.append(json.load(file))

    return incidents