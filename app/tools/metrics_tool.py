import json

from pathlib import Path


METRICS_DIR = Path(
    "data/metrics"
)


def load_metrics():

    metrics_data = []

    for file_path in METRICS_DIR.glob(
        "*.json"
    ):

        with open(file_path, "r") as file:

            metrics = json.load(file)

            metrics_data.append(metrics)

    return metrics_data