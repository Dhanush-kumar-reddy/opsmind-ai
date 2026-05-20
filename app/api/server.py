from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.graph.workflow import graph

app = FastAPI()


@app.get("/")
async def health_check():

    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_incident(
    incident: dict
):

    try:

        if not incident:

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Empty incident payload"
                }
            )

        required_fields = [
            "incident_id",
            "service",
            "severity",
            "description"
        ]

        missing_fields = []

        for field in required_fields:

            if field not in incident:

                missing_fields.append(field)

        if missing_fields:

            return JSONResponse(
                status_code=400,
                content={
                    "error": (
                        "Missing required fields"
                    ),
                    "missing_fields": (
                        missing_fields
                    )
                }
            )

        result = graph.invoke(incident)

        if not result:

            return JSONResponse(
                status_code=500,
                content={
                    "error": (
                        "Graph returned empty result"
                    )
                }
            )

        return result

    except Exception as error:

        print(
            "SERVER ERROR:",
            str(error)
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": str(error)
            }
        )