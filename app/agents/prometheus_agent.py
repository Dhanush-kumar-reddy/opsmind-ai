from app.integrations.prometheus_client import (
    query_prometheus
)


def analyze_prometheus_metrics():

    cpu_query = (
        '100 - (avg by(instance)'
        '(rate(node_cpu_seconds_total'
        '{mode="idle"}[5m])) * 100)'
    )

    memory_query = (
        '(1 - (node_memory_MemAvailable_bytes '
        '/ node_memory_MemTotal_bytes)) * 100'
    )

    cpu_data = query_prometheus(
        cpu_query
    )

    memory_data = query_prometheus(
        memory_query
    )

    return {
        "cpu_metrics": cpu_data,
        "memory_metrics": memory_data
    }