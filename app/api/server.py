from fastapi import FastAPI

from app.graph.workflow import graph


app = FastAPI()


@app.get("/health")

def health_check():

    return {
        "status": "healthy"
    }


@app.post("/analyze")

def analyze_incident(
    incident: dict
):

    result = graph.invoke({
        "incident": incident
    })

    return result