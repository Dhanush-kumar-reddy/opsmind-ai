def analyze_logs(retrieved_logs: list) -> dict:
    errors = []
    warnings = []
    info = []

    for log_group in retrieved_logs:
        log_file = log_group["file"]

        for entry in log_group["entries"]:
            if "ERROR" in entry:
                errors.append({
                    "file": log_file,
                    "message": entry
                })

            elif "WARNING" in entry:
                warnings.append({
                    "file": log_file,
                    "message": entry
                })

            elif "INFO" in entry:
                info.append({
                    "file": log_file,
                    "message": entry
                })

    summary = generate_summary(errors, warnings)

    return {
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "summary": summary
    }


def generate_summary(errors: list, warnings: list) -> str:
    if errors:
        return (
            f"Detected {len(errors)} errors and "
            f"{len(warnings)} warnings in system logs."
        )

    return "No major failures detected."