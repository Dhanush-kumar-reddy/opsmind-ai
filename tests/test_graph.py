from app.graph.workflow import graph


initial_state = {
    "incident": {
        "incident_id": "TEST001",
        "service": "Auth API",
        "severity": "High",
        "description": (
            "Users unable to login "
            "after deployment"
        )
    }
}


print("Starting graph...")

result = graph.invoke(initial_state)

print("Graph completed.")

print(result)