from app.loaders.incident_loader import load_incident

from app.graph.workflow import graph


def main():

    incident = load_incident(
        "incident_001.json"
    )

    initial_state = {
        "incident": incident
    }

    result = graph.invoke(initial_state)

    print("\nFINAL INCIDENT REPORT\n")

    for key, value in result["summary_result"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()