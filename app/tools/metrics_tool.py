import json

from pathlib import Path


from app.core.config import (
    METRICS_DIR
)


def load_metrics():

    metrics_data = []

    for file_path in METRICS_DIR.glob(
        "*.json"
    ):

        try:

            with open(
                file_path,
                "r"
            ) as file:

                metrics = json.load(file)

                if isinstance(
                    metrics,
                    list
                ):

                    for item in metrics:

                        if isinstance(
                            item,
                            dict
                        ):

                            metrics_data.append(
                                item
                            )

                elif isinstance(
                    metrics,
                    dict
                ):

                    metrics_data.append(
                        metrics
                    )

        except Exception as error:

            print(
                f"Failed loading metrics "
                f"from {file_path}: {error}"
            )

    return metrics_data