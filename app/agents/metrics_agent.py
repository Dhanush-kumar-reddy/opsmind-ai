import json

from pathlib import Path


METRICS_DIR = Path("data/metrics")


def analyze_metrics():

    findings = []

    for file_path in METRICS_DIR.glob("*.json"):

        with open(file_path, "r") as file:
            metrics = json.load(file)

        if metrics["cpu_usage"] > 85:

            findings.append(
                f"{metrics['service']} CPU usage critical."
            )

        if metrics["error_rate"] > 20:

            findings.append(
                f"{metrics['service']} error rate elevated."
            )

        if metrics["healthy_instances"] < (
            metrics["total_instances"] / 2
        ):

            findings.append(
                f"{metrics['service']} unhealthy instances detected."
            )

    return {
        "metrics_findings": findings
    }