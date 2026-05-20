import traceback

from fastapi import FastAPI
from fastapi import HTTPException

from app.graph.workflow import graph

app = FastAPI()


@app.get("/")
def health_check():

    return {
        "status": "healthy",
        "service": "OpsMind AI"
    }


@app.post("/analyze")
def analyze_incident(incident: dict):

    try:

        result = graph.invoke({
            "incident": incident
        })

        if not isinstance(result, dict):

            raise Exception(
                "Workflow returned invalid result"
            )

        if "summary_result" not in result:

            raise Exception(
                "summary_result missing"
            )

        if "retrieval_result" not in result:

            result["retrieval_result"] = {
                "relevant_logs": [],
                "relevant_docs": []
            }

        return result

    except Exception as error:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Workflow Failed: {error}"
        )